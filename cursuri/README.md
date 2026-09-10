# ML pentru Olimpiada

## De ce?

Inca ezit putin sa ma apuc de el deoarece:

Nu sunt foarte convins ca numele *AI* descrie ceea ce facem prin aceste metode. Mi se pare, de multe ori, o umbra palida a cognitiei: luam lucruri extrem de complexe si le trecem printr-un model surogat, optimizat pentru un proxy care nu surprinde neaparat ceea ce ne intereseaza cu adevarat. Iar termenul este folosit foarte des cu o conotatie mult mai pretentioasa decat continutul real.

Mai important, cred ca o olimpiada de ML risca sa puna prea mult accent pe **cum facem ceva** si prea putin pe **de ce facem acel lucru**.

La informatica, o metrica este de obicei destul de cinstita: o solutie corecta este corecta. In ML, lucrurile sunt mai ample. Poti ajunge sa optimizezi o metrica care este doar un proxy pentru un obiectiv mult mai complex, iar raspunsul la o problema poate deveni pur si simplu „facem o retea mai mare”. In industrie se ajunge uneori sa construim sisteme care optimizeaza foarte bine lucruri care poate nu ar fi trebuit optimizate in primul rand.

De asta vreau ca acest curs sa fie mai mult decat o colectie de algoritmi si trucuri pentru olimpiada.

**Magia apare atunci cand intelegi ce poti sa rezolvi, cum poti sa rezolvi si, mai ales, de ce merita sa rezolvi problema respectiva.**

## Ce incerc sa insirui:

Un parcurs de la zero pana la nivel de olimpiada, care va evolua pe parcurs. E facut din ce descriu ei pe ONIA, dar nu imi place ordinea in care se face asta neaparat

Fiecare capitol bifat e un folder cu `README.md` (teorie) + `exercitii.md`
(exercitii, fiecare cu link catre notebook-ul lui in `notebooks/`).

- [Python, NumPy, Pandas](fundamentals/README.md)
- Prelucrarea si vizualizarea datelor
- Machine Learning fundamentals
- Regresie si clasificare
- Decision Trees, Random Forest, Gradient Boosting, SVM, KNN
- Clustering si PCA
- Feature engineering
- Train/validation/test si cross-validation
- Overfitting, underfitting si regularizare
- Metrici: Accuracy, Precision, Recall, F1, ROC-AUC, MSE, MAE, RMSE, R²
- Hyperparameter tuning
- Neural Networks si PyTorch
- Computer Vision
- NLP
- Probleme si exercitii de tip olimpiada

Structura exacta nu este batuta in cuie. Cursul se va construi pe masura ce vedem ce este util, ce este dificil si ce merita aprofundat.

## Referinte

- [Programa oficiala a Olimpiadei Nationale de Inteligenta Artificiala](https://platform.olimpiada-ai.ro/ro/roadmap/programa)