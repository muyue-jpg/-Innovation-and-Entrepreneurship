mod = 2


# func1:求乘法的逆
def GCD(n1, n2):
    if n1 < n2:
        n1, n2 = n2, n1
    while n2:
        n1, n2 = n2, n1 % n2
    return n1


def EX_GCD(n1, n2, arr):  # 扩展欧几里得
    if n2 == 0:
        arr[0] = 1
        arr[1] = 0
        return n1
    g = EX_GCD(n2, n1 % n2, arr)
    t = arr[0]
    arr[0] = arr[1]
    arr[1] = t - int(n1 / n2) * arr[1]
    return g


def ModReverse(n1, n2):  # ax=1(mod n) 求a模n的乘法逆x
    arr = [0, 1, ]
    gcd = EX_GCD(n1, n2, arr)
    if gcd == 1:
        return (arr[0] % n2 + n2) % n2
    else:
        return -1


# func2:有限域加法
def Addition(p, q):
    if p == q:
        n1 = (3 * pow(p[0], 2) + a)
        n2 = (2 * p[1])
        if n1 % n2 != 0:
            val = ModReverse(n2, mod)
            y = (n1 * val) % mod
        else:
            y = (n1 / n2) % mod
    else:
        n1 = (p[1] - q[1])
        n2 = (p[0] - q[0])
        if GCD(n2, mod) != 1 and GCD(n2, mod) != -1:
            return 0
        else:
            val = ModReverse(n2, mod)
            y = (n1 * val) % mod

    arr = []
    Rx = (pow(y, 2) - p[0] - q[0]) % mod
    Ry = (y * (p[0] - Rx) - p[1]) % mod
    arr.append(Rx)
    arr.append(Ry)
    return arr


# func3：有限域乘法
def Multiplication(N, p):
    if N == 0:
        return 0
    if N == 1:
        return p
    q = p
    while N >= 2:
        q = Addition(q, p)
        N = N - 1
    return q


# func4:签名算法 Key Gen: P=dG), n is order,R=kG

def Sign(m, n, d, G, k):  # Sign(message,modulus,)
    R = Multiplication(k, G)
    r = R[0] % n
    e = hash(m)
    s = (ModReverse(k, n) * (e + d * r)) % n
    return r, s


# func5:验证算法 （r,s）of M with P
def Verify(m, n, r, s, G, P):
    e = hash(m)
    w = ModReverse(s, n)
    arr = Addition(Multiplication((e * w) % n, G), Multiplication((r * w) % n, P))  # (r',s'=e·wG+r·wP)
    if arr[0] % n == r:
        print("success")
        return True
    else:
        print("false")
        return False


# Leaking k leads to leaking of d)
def leaking_k(m, n, r, s, k):
    e = hash(m)  # s = (ModReverse(k, n) * (e + d * r)) % n
    temp = ModReverse(r, n)
    d = temp * (k * s - e) % n
    return d
