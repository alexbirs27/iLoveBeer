def suma_cifre(n):
    s = 0
    while n > 0:
        s += n % 10
        n //= 10
    return s

suma_cifre(12345)  # 15
