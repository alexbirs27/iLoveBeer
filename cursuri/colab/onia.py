"""Utilitare pentru colab-urile cursului: vizualizator pas cu pas, verificator de exercitii, descarcare de fisiere.

In notebook:
    from onia import *

    %%vezi            <- pune asta pe prima linie a unei celule si vezi cum se executa codul
    verifica(...)     <- verifica un exercitiu
"""
import builtins
import contextlib
import copy
import html as _html
import inspect
import io
import json
import os
import shlex
import shutil
import signal
import sys
import types
import urllib.request
import uuid

from IPython import get_ipython
from IPython.display import HTML, display

BAZA = os.environ.get('ONIA_BAZA', 'https://raw.githubusercontent.com/alexbirs27/iLoveBeer/main/cursuri/colab/')

__all__ = ['vezi', 'vezi_html', 'verifica', 'verifica_program', 'verifica_egal', 'scor', 'asigura_toate',
           'descarca', 'reseteaza_scor']


def descarca(*fisiere):
    """Aduce fisierele (de ex. 'date/elevi.csv') langa notebook, daca nu exista deja."""
    for f in fisiere:
        if os.path.exists(f):
            continue
        os.makedirs(os.path.dirname(f) or '.', exist_ok=True)
        if os.path.isdir(BAZA):
            shutil.copy(os.path.join(BAZA, f), f)
        else:
            urllib.request.urlretrieve(BAZA + f, f)


# ---------------------------------------------------------------------------
# Vizualizator pas cu pas
# ---------------------------------------------------------------------------

class _Oprit(BaseException):
    pass


_MAX_ELEM = 30
_MAX_ADANC = 4


def _scurt(r, lim):
    return r if len(r) <= lim else r[:lim - 3] + '...'


def _nod(v, ctx, cale=(), adanc=0):
    """Transforma o valoare Python intr-un arbore JSON usor de desenat."""
    if type(v).__module__ == 'numpy' and getattr(v, 'ndim', 1) == 0 and hasattr(v, 'item'):
        v = v.item()
    t = type(v)
    if v is None or t in (int, float, bool, complex):
        return {'k': 'p', 'r': repr(v), 'ty': 'None' if v is None else t.__name__}
    if t is str:
        return {'k': 'p', 'r': _scurt(repr(v), 60), 'ty': 'str'}
    if adanc >= _MAX_ADANC:
        return {'k': 'x', 'r': '...'}
    if type(v).__module__ == 'numpy' and hasattr(v, 'tolist') and getattr(v, 'ndim', 0) in (1, 2) and v.size <= 200:
        return _nod_lista(v.tolist(), 'array', ctx, cale, adanc, id(v))
    if isinstance(v, (list, tuple)):
        return _nod_lista(v, t.__name__ if t in (list, tuple) else 'list', ctx, cale, adanc, id(v))
    if isinstance(v, (set, frozenset)):
        items = sorted(v, key=repr) if len(v) <= _MAX_ELEM else list(v)[:_MAX_ELEM]
        return _cont({'k': 's', 'it': [_nod(x, ctx, cale + (id(v),), adanc + 1) for x in items],
                      'more': max(0, len(v) - _MAX_ELEM)}, v, ctx)
    if isinstance(v, dict):
        if id(v) in cale:
            return {'k': 'x', 'r': '{...}'}
        items = list(v.items())[:_MAX_ELEM]
        return _cont({'k': 'd', 'it': [[_nod(a, ctx, cale + (id(v),), adanc + 1), _nod(b, ctx, cale + (id(v),), adanc + 1)]
                                       for a, b in items], 'more': max(0, len(v) - _MAX_ELEM)}, v, ctx)
    if isinstance(v, types.FunctionType):
        try:
            return {'k': 'f', 'r': f'def {v.__name__}{inspect.signature(v)}'}
        except (TypeError, ValueError):
            return {'k': 'f', 'r': f'def {v.__name__}(...)'}
    if isinstance(v, type):
        return {'k': 'f', 'r': f'class {v.__name__}'}
    if hasattr(v, '__dict__') and type(v).__module__ == '__main__':
        if id(v) in cale:
            return {'k': 'x', 'r': type(v).__name__ + '(...)'}
        at = [[n, _nod(x, ctx, cale + (id(v),), adanc + 1)] for n, x in list(vars(v).items())[:_MAX_ELEM]
              if not n.startswith('__')]
        return _cont({'k': 'o', 'cls': type(v).__name__, 'at': at}, v, ctx)
    return {'k': 'x', 'r': _scurt(repr(v), 60)}


def _nod_lista(v, ty, ctx, cale, adanc, ident):
    if ident in cale:
        return {'k': 'x', 'r': '[...]'}
    it = [_nod(x, ctx, cale + (ident,), adanc + 1) for x in list(v)[:_MAX_ELEM]]
    return _cont({'k': 'l', 'ty': ty, 'it': it, 'more': max(0, len(v) - _MAX_ELEM)}, v, ctx, ident)


def _cont(nod, v, ctx, ident=None):
    ident = id(v) if ident is None else ident
    nod['i'] = ident
    ctx['cnt'][ident] = ctx['cnt'].get(ident, 0) + 1
    return nod


def _finalizeaza(nod, ctx):
    """Pune eticheta @n doar pe containerele care apar in mai multe locuri (aliasing)."""
    if isinstance(nod, dict):
        i = nod.pop('i', None)
        if i is not None and ctx['cnt'].get(i, 0) > 1:
            nod['sh'] = ctx['lab'].setdefault(i, '@%d' % (len(ctx['lab']) + 1))
        for v in nod.values():
            _finalizeaza(v, ctx)
    elif isinstance(nod, list):
        for v in nod:
            _finalizeaza(v, ctx)


def _colecteaza(cod, inputs, max_pasi):
    fn = '<vezi>'
    pasi = []
    buf = io.StringIO()
    ctx_lab = {}
    fids = {}
    contor = [0]

    try:
        code = compile(cod, fn, 'exec')
    except SyntaxError as e:
        return [{'l': e.lineno, 'fr': [], 'o': 0, 'err': f'SyntaxError: {e.msg}'}], ''

    def stiva(frame):
        cadre = []
        f = frame
        while f is not None:
            if f.f_code.co_filename == fn:
                cadre.append(f)
            f = f.f_back
        cadre.reverse()
        return cadre

    def instantaneu(frame):
        ctx = {'cnt': {}, 'lab': ctx_lab}
        cadre = []
        for f in stiva(frame):
            glob = f.f_code.co_name == '<module>'
            d = dict(f.f_globals) if glob else dict(f.f_locals)
            vs = []
            for n, v in d.items():
                if n.startswith('__') or n.startswith('.') or isinstance(v, types.ModuleType):
                    continue
                vs.append([n, _nod(v, ctx)])
            cadre.append({'id': fids.get(id(f), 0), 'n': 'Global' if glob else f.f_code.co_name, 'v': vs})
        _finalizeaza(cadre, ctx)
        return cadre

    def tracer(frame, event, arg):
        if frame.f_code.co_filename != fn:
            return None
        if event == 'call':
            contor[0] += 1
            fids[id(frame)] = contor[0]
        elif event == 'line':
            if len(pasi) >= max_pasi:
                raise _Oprit()
            pasi.append({'l': frame.f_lineno, 'fr': instantaneu(frame), 'o': len(buf.getvalue())})
        elif event == 'return':
            if frame.f_code.co_name != '<module>':
                if len(pasi) >= max_pasi:
                    raise _Oprit()
                pasi.append({'l': frame.f_lineno, 'fr': instantaneu(frame), 'o': len(buf.getvalue()),
                             'rv': _scurt(repr(arg), 50)})
        return tracer

    def _input(prompt=''):
        buf.write(str(prompt))
        if not inputs:
            raise EOFError('input() cere o valoare, dar nu ai dat destule valori de intrare')
        v = inputs.pop(0)
        buf.write(str(v) + '\n')
        return str(v)

    bi = dict(vars(builtins))
    bi['input'] = _input
    g = {'__builtins__': bi, '__name__': '__main__'}
    err = None
    oprit = False

    sys.settrace(tracer)
    try:
        with contextlib.redirect_stdout(buf):
            exec(code, g)
    except _Oprit:
        oprit = True
    except BaseException as e:  # noqa: BLE001 - vrem sa aratam orice eroare din codul elevului
        tb = e.__traceback__
        linie = None
        while tb is not None:
            if tb.tb_frame.f_code.co_filename == fn:
                linie = tb.tb_lineno
            tb = tb.tb_next
        err = (f'{type(e).__name__}: {e}', linie)
    finally:
        sys.settrace(None)

    ctx = {'cnt': {}, 'lab': ctx_lab}
    if not oprit:
        # starea finala, dupa ultima linie: refolosim variabilele globale din g
        vs = []
        for n, v in g.items():
            if n.startswith('__') or isinstance(v, types.ModuleType):
                continue
            vs.append([n, _nod(v, ctx)])
        _finalizeaza(vs, ctx)
        pas = {'l': None, 'fr': [{'id': 1, 'n': 'Global', 'v': vs}], 'o': len(buf.getvalue()), 'sfarsit': True}
        if err:
            pas['err'] = err[0]
            pas['l'] = err[1]
        pasi.append(pas)
    else:
        pasi[-1]['oprit'] = True
    return pasi, buf.getvalue()


_CSS = """
#ID{font-family:system-ui,-apple-system,'Segoe UI',Roboto,sans-serif;background:#fff;color:#1f2933;border:1px solid #d5dbe3;border-radius:10px;padding:10px;max-width:1000px;font-size:14px;outline:none}
#ID *{box-sizing:border-box}
#ID .ov-bar{display:flex;flex-wrap:wrap;gap:6px;align-items:center;margin-bottom:8px}
#ID button{background:#eef2f7;border:1px solid #c5cdd8;border-radius:6px;padding:4px 10px;cursor:pointer;font-size:13px;color:#1f2933}
#ID button:hover{background:#dde5ef}
#ID select{font-size:13px;padding:2px;border-radius:6px;border:1px solid #c5cdd8;background:#fff;color:#1f2933}
#ID .ov-sl{flex:1 1 120px;min-width:100px}
#ID .ov-cnt{font-size:12px;color:#52606d;min-width:74px}
#ID .ov-body{display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1fr);gap:10px}
@media(max-width:700px){#ID .ov-body{grid-template-columns:1fr}}
#ID .ov-h{font-size:11px;font-weight:600;letter-spacing:.06em;text-transform:uppercase;color:#7b8794;margin-bottom:4px}
#ID .ov-code{font-family:ui-monospace,Menlo,Consolas,monospace;font-size:13px;background:#f8fafc;border:1px solid #e2e8f0;border-radius:8px;padding:6px 0;overflow:auto;max-height:440px}
#ID .ov-ln{display:flex;white-space:pre;padding:1px 8px 1px 0;border-left:4px solid transparent;line-height:1.5}
#ID .ov-ln .nr{width:34px;text-align:right;color:#9aa5b1;padding-right:10px;flex:none;user-select:none}
#ID .ov-ln.prev{background:#e6fcf5;border-left-color:#20c997}
#ID .ov-ln.cur{background:#fff3bf;border-left-color:#f59f00}
#ID .ov-ln.errl{background:#ffe3e3;border-left-color:#e03131}
#ID .k{color:#c2255c;font-weight:600}#ID .s{color:#2b8a3e}#ID .c{color:#868e96;font-style:italic}#ID .n{color:#1971c2}#ID .d{color:#7048e8;font-weight:600}
#ID .ov-mem{background:#f8fafc;border:1px solid #e2e8f0;border-radius:8px;padding:8px;overflow:auto;max-height:440px}
#ID .ov-frame{background:#fff;border:1px solid #e2e8f0;border-radius:8px;padding:6px 8px;margin-bottom:8px}
#ID .ov-frame.act{border-color:#f59f00;box-shadow:0 0 0 2px #fff3bf}
#ID .ov-fh{font-family:ui-monospace,Menlo,Consolas,monospace;font-size:12px;font-weight:700;color:#495057;margin-bottom:4px}
#ID .ov-var{display:flex;align-items:flex-start;gap:8px;padding:3px 0;border-top:1px dashed #edf0f4}
#ID .ov-var:first-of-type{border-top:none}
#ID .ov-vn{font-family:ui-monospace,Menlo,Consolas,monospace;font-weight:700;min-width:56px;padding-top:3px}
#ID .ov-empty{color:#9aa5b1;font-size:12px;font-style:italic}
#ID .p{display:inline-block;font-family:ui-monospace,Menlo,Consolas,monospace;font-size:13px;padding:2px 7px;border-radius:5px;border:1px solid transparent}
#ID .p.int,#ID .p.float,#ID .p.complex{background:#e7f1ff;color:#1c5fb5;border-color:#c5dcf8}
#ID .p.str{background:#e6f6ec;color:#22703c;border-color:#c3e6cf}
#ID .p.bool{background:#fff0e0;color:#b35a00;border-color:#f6d5ad}
#ID .p.None{background:#eceff3;color:#5c6773;border-color:#d5dbe3}
#ID .box{display:inline-block;position:relative;vertical-align:top;border:1px solid #cbd2d9;border-radius:6px;padding:14px 6px 5px;background:#fff}
#ID .tg{position:absolute;top:1px;left:6px;font-size:9px;font-weight:700;letter-spacing:.05em;text-transform:uppercase;color:#9aa5b1}
#ID .sh{position:absolute;top:1px;right:6px;font-size:10px;font-weight:700;color:#fff;background:#7048e8;border-radius:8px;padding:0 6px}
#ID .row{display:flex;flex-wrap:wrap;gap:4px;align-items:flex-end}
#ID .cell{display:flex;flex-direction:column;align-items:center}
#ID .ix{font-size:10px;color:#9aa5b1;font-family:ui-monospace,Menlo,Consolas,monospace}
#ID .cellv{min-width:30px;text-align:center;border:1px solid #cbd2d9;border-radius:4px;padding:2px 4px;background:#fdfdfe}
#ID table.mt{border-collapse:separate;border-spacing:3px}
#ID table.mt td,#ID table.mt th{font-family:ui-monospace,Menlo,Consolas,monospace;font-size:12px;text-align:center;padding:2px 6px}
#ID table.mt th{color:#9aa5b1;font-weight:400;font-size:10px}
#ID table.mt td{border:1px solid #cbd2d9;border-radius:4px;background:#fdfdfe;min-width:28px}
#ID table.dt{border-collapse:separate;border-spacing:0 3px}
#ID table.dt td{padding:0 6px 0 0;vertical-align:top}
#ID .arrow{color:#9aa5b1;padding:2px 4px}
#ID .ov-note{margin-top:8px;min-height:22px;font-size:13.5px;color:#243b53;background:#eef6ff;border-left:4px solid #74a7ff;border-radius:4px;padding:5px 9px}
#ID .ov-note.err{background:#ffe3e3;border-left-color:#e03131;color:#a61e1e}
#ID .ov-note.hid{visibility:hidden}
#ID .ov-out{margin:8px 0 0;background:#1e2430;color:#e6edf3;font-family:ui-monospace,Menlo,Consolas,monospace;font-size:13px;border-radius:8px;padding:8px 10px;min-height:38px;white-space:pre-wrap;max-height:220px;overflow:auto}
#ID .ov-out i{color:#7d8896}
@keyframes ovflash{0%{background:#ffd43b;transform:scale(1.18)}100%{transform:none}}
@keyframes ovin{0%{opacity:0;transform:translateY(-7px)}100%{opacity:1;transform:none}}
#ID .chg{animation:ovflash .9s ease-out}
#ID .new{animation:ovin .55s ease-out}
"""

_JS = r"""
(function(){
const D = __DATA__;
const root = document.getElementById('__ID__');
const $ = s => root.querySelector(s);
let i = 0, timer = null;
const KW = new Set(['def','class','if','elif','else','for','while','in','not','and','or','return','import','from','as','True','False','None','break','continue','pass','lambda','try','except','finally','with','raise','is','yield','global','nonlocal','assert','del']);
const esc = s => s.replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;');
function hl(line){
  const re = /(#.*)|('(?:\\.|[^'\\])*'|"(?:\\.|[^"\\])*")|\b([A-Za-z_][A-Za-z_0-9]*)\b|\b(\d+\.?\d*)\b/g;
  let out = '', last = 0, m;
  while((m = re.exec(line))){
    out += esc(line.slice(last, m.index));
    if(m[1]) out += '<span class="c">'+esc(m[1])+'</span>';
    else if(m[2]) out += '<span class="s">'+esc(m[2])+'</span>';
    else if(m[3]) out += KW.has(m[3]) ? '<span class="k">'+m[3]+'</span>' : esc(m[3]);
    else out += '<span class="n">'+m[4]+'</span>';
    last = re.lastIndex;
  }
  return out + esc(line.slice(last));
}
const eq = (a,b) => JSON.stringify(a) === JSON.stringify(b);
function flash(n,p){ return p === undefined ? ' new' : (eq(n,p) ? '' : ' chg'); }
function sh(n){ return n.sh ? '<span class="sh">'+n.sh+'</span>' : ''; }
function isMat(n){
  return n.k==='l' && n.it.length>0 && n.it.every(r => r.k==='l' && r.it.every(x => x.k==='p'));
}
function rnd(n, p){
  if(n.k==='p') return '<span class="p '+n.ty+flash(n,p)+'">'+esc(n.r)+'</span>';
  if(n.k==='f') return '<span class="p None'+flash(n,p)+'">'+esc(n.r)+'</span>';
  if(n.k==='x') return '<span class="p None">'+esc(n.r)+'</span>';
  if(n.k==='l'){
    if(isMat(n)){
      const pm = p && isMat(p) ? p : null;
      const cols = Math.max(...n.it.map(r => r.it.length));
      let h = '<span class="box'+(p===undefined?' new':'')+'"><span class="tg">'+n.ty+'</span>'+sh(n)+'<table class="mt"><tr><th></th>';
      for(let c=0;c<cols;c++) h += '<th>'+c+'</th>';
      h += '</tr>';
      n.it.forEach((r,ri) => {
        h += '<tr><th>'+ri+(r.sh ? ' <span class="sh" style="position:static;display:inline-block">'+r.sh+'</span>' : '')+'</th>';
        r.it.forEach((x,ci) => {
          const px = pm && pm.it[ri] && pm.it[ri].it[ci];
          h += '<td class="'+(pm ? (px===undefined?'new':(eq(x,px)?'':'chg')) : '')+'">'+esc(x.r)+'</td>';
        });
        h += '</tr>';
      });
      return h + '</table></span>';
    }
    const pl = p && p.k==='l' ? p : null;
    let h = '<span class="box'+(p===undefined?' new':'')+'"><span class="tg">'+n.ty+'</span>'+sh(n)+'<span class="row">';
    if(!n.it.length) h += '<span class="ov-empty">gol</span>';
    n.it.forEach((x,j) => {
      const px = pl ? pl.it[j] : undefined;
      const inner = x.k==='p' ? '<span class="cellv'+(pl ? flash(x,px) : '')+'">'+esc(x.r)+'</span>' : rnd(x, pl ? px : undefined);
      h += '<span class="cell"><span class="ix">'+j+'</span>'+inner+'</span>';
    });
    if(n.more) h += '<span class="ov-empty">... +'+n.more+'</span>';
    return h + '</span></span>';
  }
  if(n.k==='s'){
    const ps = p && p.k==='s' ? p : null;
    const old = new Set(ps ? ps.it.map(x => x.r) : []);
    let h = '<span class="box'+(p===undefined?' new':'')+'"><span class="tg">set</span>'+sh(n)+'<span class="row">';
    if(!n.it.length) h += '<span class="ov-empty">gol</span>';
    n.it.forEach(x => { h += '<span class="p '+(x.ty||'int')+(ps && !old.has(x.r) ? ' new' : '')+'">'+esc(x.r)+'</span>'; });
    return h + '</span></span>';
  }
  if(n.k==='d'){
    const pd = p && p.k==='d' ? p : null;
    const old = {};
    if(pd) pd.it.forEach(kv => old[kv[0].r] = kv[1]);
    let h = '<span class="box'+(p===undefined?' new':'')+'"><span class="tg">dict</span>'+sh(n)+'<table class="dt">';
    if(!n.it.length) h += '<tr><td><span class="ov-empty">gol</span></td></tr>';
    n.it.forEach(kv => {
      const pv = pd ? old[kv[0].r] : undefined;
      h += '<tr><td>'+rnd(kv[0], undefined).replace(' new','')+'</td><td class="arrow">&rarr;</td><td>'+rnd(kv[1], pd ? pv : undefined)+'</td></tr>';
    });
    return h + '</table></span>';
  }
  if(n.k==='o'){
    const po = p && p.k==='o' ? p : null;
    const old = {};
    if(po) po.at.forEach(a => old[a[0]] = a[1]);
    let h = '<span class="box'+(p===undefined?' new':'')+'"><span class="tg">'+esc(n.cls)+'</span>'+sh(n)+'<table class="dt">';
    n.at.forEach(a => {
      h += '<tr><td><b style="font-family:monospace">'+esc(a[0])+'</b></td><td class="arrow">&rarr;</td><td>'+rnd(a[1], po ? old[a[0]] : undefined)+'</td></tr>';
    });
    return h + '</table></span>';
  }
  return '';
}
function build(){
  const cod = $('.ov-code');
  cod.innerHTML = D.cod.map((t,j) => '<div class="ov-ln" data-l="'+(j+1)+'"><span class="nr">'+(j+1)+'</span><span class="tx">'+hl(t)+'</span></div>').join('');
  const sl = $('.ov-sl'); sl.max = D.pasi.length-1;
}
function show(){
  const s = D.pasi[i], pv = i>0 ? D.pasi[i-1] : null;
  root.querySelectorAll('.ov-ln').forEach(e => e.className = 'ov-ln');
  const el = s.l ? root.querySelector('.ov-ln[data-l="'+s.l+'"]') : null;
  if(pv && pv.l && !(s.sfarsit && s.err)) { const e2 = root.querySelector('.ov-ln[data-l="'+pv.l+'"]'); if(e2) e2.classList.add('prev'); }
  if(el){
    el.classList.remove('prev'); el.classList.add(s.err ? 'errl' : 'cur');
    const c = $('.ov-code');
    if(el.offsetTop < c.scrollTop || el.offsetTop+el.offsetHeight > c.scrollTop+c.clientHeight) c.scrollTop = Math.max(0, el.offsetTop - c.clientHeight/2);
  }
  const prevFr = {};
  if(pv) pv.fr.forEach(f => { const m = {}; f.v.forEach(v => m[v[0]] = v[1]); prevFr[f.id] = m; });
  let h = '';
  s.fr.forEach((f, fi) => {
    h += '<div class="ov-frame'+(fi===s.fr.length-1 ? ' act' : '')+'"><div class="ov-fh">'+esc(f.n === 'Global' ? 'Global' : f.n+'()')+'</div>';
    if(!f.v.length) h += '<div class="ov-empty">nicio variabila inca</div>';
    f.v.forEach(v => {
      const pm = prevFr[f.id];
      const pn = pm ? pm[v[0]] : undefined;
      h += '<div class="ov-var"><span class="ov-vn">'+esc(v[0])+'</span><span>'+rnd(v[1], pv ? pn : v[1])+'</span></div>';
    });
    h += '</div>';
  });
  $('.ov-mem').innerHTML = '<div class="ov-h">Memorie</div>' + h;
  const out = D.out.slice(0, s.o);
  $('.ov-out').innerHTML = out ? esc(out) : '<i>(nimic afisat inca)</i>';
  const note = $('.ov-note');
  let txt = '', cls = 'ov-note';
  if(s.err){ txt = 'Eroare: '+s.err; cls += ' err'; }
  else if(s.oprit){ txt = 'Am oprit dupa '+D.pasi.length+' pasi (prea multi ca sa-i afisam pe toti).'; }
  else if(s.rv !== undefined){ txt = 'Functia se termina si returneaza '+s.rv+'.'; }
  else if(s.sfarsit){ txt = 'Programul s-a terminat.'; }
  else if(s.l && D.note[s.l]){ txt = D.note[s.l]; }
  else { cls += ' hid'; txt = '.'; }
  note.className = cls; note.textContent = txt;
  $('.ov-sl').value = i;
  $('.ov-cnt').textContent = 'pasul '+(i+1)+' / '+D.pasi.length;
}
function go(k){ i = Math.max(0, Math.min(D.pasi.length-1, k)); show(); }
function stop(){ if(timer){ clearInterval(timer); timer = null; } $('[data-a=play]').textContent = 'Porneste'; }
function play(){
  if(timer){ stop(); return; }
  if(i >= D.pasi.length-1) i = 0;
  $('[data-a=play]').textContent = 'Pauza';
  const ms = +$('.ov-sp').value;
  timer = setInterval(() => { if(i >= D.pasi.length-1){ stop(); return; } go(i+1); }, ms);
  go(i);
}
root.addEventListener('click', e => {
  const a = e.target.getAttribute && e.target.getAttribute('data-a');
  if(!a) return;
  if(a==='first'){ stop(); go(0); } else if(a==='last'){ stop(); go(D.pasi.length-1); }
  else if(a==='prev'){ stop(); go(i-1); } else if(a==='next'){ stop(); go(i+1); } else if(a==='play') play();
});
$('.ov-sl').addEventListener('input', e => { stop(); go(+e.target.value); });
$('.ov-sp').addEventListener('change', () => { if(timer){ stop(); play(); } });
root.tabIndex = 0;
root.addEventListener('keydown', e => { if(e.key==='ArrowRight'){ stop(); go(i+1); } else if(e.key==='ArrowLeft'){ stop(); go(i-1); } });
build();
const m = (location.hash||'').match(/pas=(\d+)/);
go(m ? +m[1] : 0);
})();
"""


def _extrage_note(cod):
    """Comentariile de forma '#: text' devin explicatii afisate sub cod, cand se executa linia respectiva."""
    linii, note = [], {}
    for n, l in enumerate(cod.split('\n'), 1):
        if '#:' in l:
            l, _, t = l.partition('#:')
            note[n] = t.strip()
            l = l.rstrip()
        linii.append(l)
    return linii, note


def vezi_html(cod, inputs=None, max_pasi=250, note=None):
    """Executa 'cod' pas cu pas si intoarce HTML-ul vizualizatorului."""
    cod = cod.strip('\n')
    linii, note_cod = _extrage_note(cod)
    note_cod.update(note or {})
    pasi, out = _colecteaza('\n'.join(linii), list(inputs or []), max_pasi)
    ident = 'ov' + uuid.uuid4().hex[:10]
    date = {'cod': linii, 'pasi': pasi, 'out': out, 'note': {str(k): v for k, v in note_cod.items()}}
    js = json.dumps(date).replace('</', '<\\/')
    corp = (
        '<div class="ov-bar">'
        '<button data-a="first">|&lt;</button><button data-a="prev">&lt; Inapoi</button>'
        '<button data-a="play">Porneste</button><button data-a="next">Inainte &gt;</button>'
        '<button data-a="last">&gt;|</button>'
        '<input type="range" min="0" max="0" value="0" class="ov-sl"><span class="ov-cnt"></span>'
        '<select class="ov-sp"><option value="1500">lent</option><option value="900" selected>normal</option>'
        '<option value="450">rapid</option></select></div>'
        '<div class="ov-body"><div><div class="ov-h">Cod</div><div class="ov-code"></div></div>'
        '<div class="ov-mem"></div></div>'
        '<div class="ov-note hid">.</div>'
        '<div class="ov-h" style="margin-top:8px">Afisare</div><pre class="ov-out"></pre>'
    )
    return (f'<div id="{ident}">' + f'<style>{_CSS.replace("#ID", "#" + ident)}</style>' + corp +
            f'<script>{_JS.replace("__DATA__", js).replace("__ID__", ident)}</script></div>')


def vezi(cod, inputs=None, max_pasi=250, note=None):
    """Vizualizeaza executia pas cu pas a codului (un string). Pe scurt, in notebook: %%vezi"""
    display(HTML(vezi_html(cod, inputs, max_pasi, note)))


def _inregistreaza_magia():
    ip = get_ipython()
    if ip is None:
        return

    def vezi_magic(linie, celula):
        max_pasi, intrari = 250, []
        for t in shlex.split(linie) if linie.strip() else []:
            if t.startswith('--max='):
                max_pasi = int(t[6:])
            else:
                intrari.append(t)
        vezi(celula, inputs=intrari, max_pasi=max_pasi)

    ip.register_magic_function(vezi_magic, 'cell', 'vezi')


_inregistreaza_magia()


# ---------------------------------------------------------------------------
# Verificator de exercitii
# ---------------------------------------------------------------------------

_REG = {}


class _Timp(Exception):
    pass


def _cu_timp_fir(secunde, f, *args):
    """Varianta pentru Windows (fara SIGALRM): ruleaza f intr-un fir si ii trimite o exceptie daca depaseste timpul."""
    import ctypes
    import threading
    rez = {}

    def tinta():
        try:
            rez['v'] = f(*args)
        except BaseException as e:  # noqa: BLE001
            rez['e'] = e

    t = threading.Thread(target=tinta, daemon=True)
    t.start()
    t.join(secunde)
    if t.is_alive():
        ctypes.pythonapi.PyThreadState_SetAsyncExc(ctypes.c_ulong(t.ident), ctypes.py_object(_Timp))
        t.join(1)
        raise _Timp()
    if 'e' in rez:
        raise rez['e']
    return rez.get('v')


def _cu_timp(secunde, f, *args):
    if not hasattr(signal, 'SIGALRM'):
        return _cu_timp_fir(secunde, f, *args)

    def _handler(sig, frm):
        raise _Timp()

    vechi = signal.signal(signal.SIGALRM, _handler)
    signal.setitimer(signal.ITIMER_REAL, secunde)
    try:
        return f(*args)
    finally:
        signal.setitimer(signal.ITIMER_REAL, 0)
        signal.signal(signal.SIGALRM, vechi)


def _fmt(x, lim=90):
    return _scurt(repr(x), lim)


def _egal(a, b, tol):
    if type(a).__module__ == 'numpy' and getattr(a, 'ndim', 1) == 0 and hasattr(a, 'item'):
        a = a.item()
    if type(b).__module__ == 'numpy' and getattr(b, 'ndim', 1) == 0 and hasattr(b, 'item'):
        b = b.item()
    try:
        import numpy as np
        if isinstance(b, np.ndarray) or isinstance(a, np.ndarray):
            return isinstance(a, np.ndarray) and isinstance(b, np.ndarray) and a.shape == b.shape and \
                bool(np.allclose(a, b, atol=tol, equal_nan=True))
    except ImportError:
        pass
    if hasattr(b, 'equals'):
        if not hasattr(a, 'equals'):
            return False
        try:
            import pandas as pd
            (pd.testing.assert_frame_equal if hasattr(b, 'columns') else pd.testing.assert_series_equal)(
                a, b, atol=tol, check_dtype=False, check_names=False)
            return True
        except (AssertionError, TypeError, ValueError):
            return False
    if isinstance(b, bool) or isinstance(a, bool):
        return a is b or (isinstance(a, bool) and isinstance(b, bool) and a == b)
    if isinstance(b, float) or isinstance(a, float):
        try:
            if a != a and b != b:
                return True
            return abs(a - b) <= tol * max(1.0, abs(b))
        except TypeError:
            return False
    if isinstance(b, (list, tuple)):
        return type(a) is type(b) and len(a) == len(b) and all(_egal(x, y, tol) for x, y in zip(a, b))
    if isinstance(b, dict):
        return isinstance(a, dict) and a.keys() == b.keys() and all(_egal(a[k], b[k], tol) for k in b)
    try:
        return bool(a == b)
    except (ValueError, TypeError):
        return False


def _card(nume, ok, total, esecuri, ascunse_ok, ascunse_tot, indiciu, extra=''):
    toate = ok == total and ascunse_ok == ascunse_tot
    culoare, fond = ('#1b7f3b', '#e8f6ec') if toate else ('#b42318', '#fdecea')
    titlu = 'corect' if toate else 'mai ai de lucru'
    linii = ''.join(f'<div style="margin:2px 0;font-family:ui-monospace,Consolas,monospace;font-size:12.5px">{_html.escape(e)}</div>'
                    for e in esecuri)
    if ascunse_tot:
        linii += (f'<div style="margin-top:4px;font-size:12.5px">teste ascunse: {ascunse_ok}/{ascunse_tot} trecute</div>')
    if indiciu and not toate:
        linii += f'<div style="margin-top:6px;font-size:13px"><b>Indiciu:</b> {_html.escape(indiciu)}</div>'
    display(HTML(
        f'<div style="border-left:5px solid {culoare};background:{fond};color:#1f2933;padding:6px 10px;border-radius:6px;margin:4px 0;'
        f'font-family:system-ui,sans-serif"><b style="color:{culoare}">{_html.escape(nume)}: {titlu}</b>'
        f' <span style="font-size:13px">({ok}/{total} teste{extra})</span>{linii}</div>'))


def _inregistreaza(nume, ok_tot, tot_tot, puncte):
    _REG[nume] = {'ok': ok_tot, 'tot': tot_tot, 'p': puncte}


def _ruleaza_teste(nume, apel, teste, ascunse, indiciu, puncte, descriere, extra=''):
    """apel(args) -> (ok, detaliu). Foloseste pentru verifica() si verifica_program()."""
    ok = 0
    esecuri = []
    for args, asteptat in teste:
        good, det = apel(args, asteptat)
        ok += good
        if not good and len(esecuri) < 3:
            esecuri.append(f'{descriere(args)} -> {det}')
    ok_a = 0
    for args, asteptat in ascunse:
        good, _ = apel(args, asteptat)
        ok_a += good
    _card(nume, ok, len(teste), esecuri, ok_a, len(ascunse), indiciu, extra)
    _inregistreaza(nume, ok + ok_a, len(teste) + len(ascunse), puncte)


def verifica(nume, f, teste, ascunse=(), indiciu=None, timp=3, puncte=1, tol=1e-6, in_loc=False,
             referinta=None, generator=None, n=20):
    """Verifica functia f pe teste = [((arg1, arg2), rezultat_asteptat), ...].

    ascunse: teste suplimentare, afisate doar ca numar. referinta+generator: teste aleatoare
    (generator() intoarce tuplul de argumente, referinta(*args) rezultatul corect).
    in_loc=True: compara primul argument (modificat de functie) in loc de valoarea returnata."""
    ascunse = list(ascunse)
    if referinta is not None and generator is not None:
        for _ in range(n):
            a = generator()
            a = a if isinstance(a, tuple) else (a,)
            ascunse.append((a, referinta(*copy.deepcopy(a))))

    def apel(args, asteptat):
        args = args if isinstance(args, tuple) else (args,)
        args = copy.deepcopy(args)
        try:
            obt = _cu_timp(timp, f, *args)
            if in_loc:
                obt = args[0]
        except _Timp:
            return False, 'dureaza prea mult (bucla infinita?)'
        except Exception as e:  # noqa: BLE001
            return False, f'eroare {type(e).__name__}: {e}'
        if _egal(obt, asteptat, tol):
            return True, ''
        return False, f'ai intors {_fmt(obt)}, trebuia {_fmt(asteptat)}'

    def descriere(args):
        args = args if isinstance(args, tuple) else (args,)
        return f'{getattr(f, "__name__", "f")}({", ".join(_fmt(a, 40) for a in args)})'

    _ruleaza_teste(nume, apel, [(a, e) for a, e in teste], [(a, e) for a, e in ascunse], indiciu, puncte, descriere)


def verifica_program(nume, f, cazuri, ascunse=(), indiciu=None, timp=3, puncte=1):
    """Verifica un program care citeste cu input() si afiseaza cu print().

    cazuri = [(['5', '3'], '8'), ...]  (valorile pentru input, afisarea asteptata). f = functia care ruleaza programul."""
    def apel(intrari, asteptat):
        intrari = list(intrari.split('\n')) if isinstance(intrari, str) else list(intrari)
        it = iter(intrari)
        vechi = builtins.input
        buf = io.StringIO()

        def _inp(prompt=''):
            try:
                return next(it)
            except StopIteration:
                raise EOFError('programul citeste mai multe valori decat i-am dat')

        builtins.input = _inp
        try:
            with contextlib.redirect_stdout(buf):
                _cu_timp(timp, f)
        except _Timp:
            return False, 'dureaza prea mult (bucla infinita?)'
        except Exception as e:  # noqa: BLE001
            return False, f'eroare {type(e).__name__}: {e}'
        finally:
            builtins.input = vechi
        norm = lambda s: [x.rstrip() for x in s.strip().split('\n')]  # noqa: E731
        obt = buf.getvalue()
        if norm(obt) == norm(asteptat):
            return True, ''
        return False, f'ai afisat {_fmt(obt.strip())}, trebuia {_fmt(asteptat.strip())}'

    def descriere(intrari):
        return 'input ' + _fmt(intrari, 40)

    _ruleaza_teste(nume, apel, list(cazuri), list(ascunse), indiciu, puncte, descriere)


def verifica_egal(nume, obtinut, asteptat, tol=1e-6, indiciu=None, puncte=1):
    """Compara o valoare (numar, lista, array, DataFrame...) cu cea asteptata."""
    good = _egal(obtinut, asteptat, tol)
    esec = [] if good else [f'ai {_fmt(obtinut)}, trebuia {_fmt(asteptat)}']
    _card(nume, int(good), 1, esec, 0, 0, indiciu)
    _inregistreaza(nume, int(good), 1, puncte)


def reseteaza_scor():
    _REG.clear()


def scor():
    """Tabel cu toate exercitiile verificate pana acum si punctajul."""
    total = sum(v['p'] for v in _REG.values())
    castigat = sum(v['p'] * v['ok'] / v['tot'] for v in _REG.values() if v['tot'])
    linii = ''.join(
        f'<tr><td style="padding:2px 10px">{_html.escape(k)}</td><td style="padding:2px 10px;text-align:right">{v["ok"]}/{v["tot"]}</td>'
        f'<td style="padding:2px 10px;text-align:right">{v["p"] * v["ok"] / v["tot"]:.1f} / {v["p"]}</td></tr>'
        for k, v in _REG.items() if v['tot'])
    procent = 100 * castigat / total if total else 0
    display(HTML(
        '<div style="background:#f8fafc;color:#1f2933;border:1px solid #d5dbe3;border-radius:8px;padding:8px 12px;max-width:520px;'
        'font-family:system-ui,sans-serif"><b>Scor</b><table style="border-collapse:collapse;font-size:13px">'
        '<tr style="color:#7b8794"><td style="padding:2px 10px">exercitiu</td><td style="padding:2px 10px;text-align:right">teste</td>'
        f'<td style="padding:2px 10px;text-align:right">puncte</td></tr>{linii}</table>'
        f'<div style="margin-top:6px"><b>Total: {castigat:.1f} / {total} ({procent:.0f}%)</b></div></div>'))


def asigura_toate():
    """Pentru validarea automata a notebook-urilor cu solutii: crapa daca vreun exercitiu nu e complet corect."""
    gresite = [k for k, v in _REG.items() if v['ok'] != v['tot']]
    assert _REG, 'nu s-a verificat niciun exercitiu'
    assert not gresite, 'exercitii care nu trec: ' + ', '.join(gresite)
    print(f'toate cele {len(_REG)} exercitii trec')
