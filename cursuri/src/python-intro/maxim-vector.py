def maxim(v):
    m = v[0]
    for x in v[1:]:
        if x > m:
            m = x
    return m

maxim([3, 7, 2, 9, 4])  # 9
