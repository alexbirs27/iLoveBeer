def numara_pare(v):
    cnt = 0
    for x in v:
        if x % 2 == 0:
            cnt += 1
    return cnt

numara_pare([1, 2, 3, 4, 5, 6])  # 3
