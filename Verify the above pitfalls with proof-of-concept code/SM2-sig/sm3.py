import re


def Shift_left(n, k):  # 循环左移k位,共32比特
    k = k % 32
    b = str(bin(n))
    b = b.split('0b')[1]
    b = (32 - len(b)) * '0' + b
    return int(b[k:] + b[:k], 2)


def cut_text(text, lenth):  # 数据按间距分组划分iv向量
    textArr = re.findall('.{' + str(lenth) + '}', text)
    textArr.append(text[(len(textArr) * lenth):])
    return textArr


# 初始值
IV = '0x7380166f4914b2b9172442d7da8a0600a96f30bc163138aae38dee4db0fb0e4e'


# 常量
def T(j):
    if j < 16:
        T = int('0x79cc4519', 16)
    if 15 < j < 64:
        T = int('0x7a879d8a', 16)
    return T


# 布尔函数
def FF(x, y, z, j):  # 布尔函数1，式中X,Y,Z 为字。
    if j <= 15:
        return x ^ y ^ z  # X ⊕ Y ⊕ Z
    if 15 < j < 64:
        return (x & y) | (y & z) | (x & z)  # (X ∧ Y ) ∨ (X ∧ Z) ∨ (Y ∧ Z )


def GG(x, y, z, j):  # 布尔函数2，式中X,Y,Z 为字。
    if j <= 15:
        return x ^ y ^ z  # X ⊕ Y ⊕ Z
    if 15 < j < 64:
        return (x & y) | (~x & z)  # (X ∧ Y ) ∨ ( ¬X∧ Z)


# 置换函数
def p0(x):  # 置换函数1，式中X为字
    return x ^ (Shift_left(x, 9)) ^ (Shift_left(x, 17))  # X ⊕ (X ≪ 9) ⊕ (X ≪ 17)


def p1(x):  # 置换函数2，式中X为字
    return x ^ (Shift_left(x, 15)) ^ (Shift_left(x, 23))  # X ⊕ (X ≪ 15) ⊕ (X ≪ 23)


def ASCII(m):  # 将message通过ASCII码转化为二进制数
    r = ""
    x = ""

    for i in m:
        l = 8 - len((x + bin(ord(i))).split('0b')[1]) % 8
        r = r + l * '0' + (x + bin(ord(i))).split('0b')[1]
    #print(r)
    return r


def HEX(m):  # 将message转化为二进制数
    r = ""
    x = ""

    for i in m:
        l = 4 - len((x + bin(int(i, 16))).split('0b')[1]) % 4
        r = r + l * '0' + (x + bin(int(i, 16))).split('0b')[1]
    #print(r)
    return r


def s2m2b(s):  # 数据m填充,分组b[i]

    k = 448 - (len(s) + 1) % 512  # l + 1 + k ≡ 448mod512
    # print(r)
    out = s + '1' + k * '0'
    length = bin(len(s)).split('0b')[1]
    t = 64 - len(length)
    out = out + t * '0' + length  # 添加一个64位比特串，该比特串是长度l的二进制表示
    # print(hex(int(out,2)))
    out = cut_text(out, 512)

    return out


def cf(v, b):
    w = cut_text(b, 32)
    w2 = []
    for j in range(16):
        w[j] = int(w[j], 2)
    del w[16]
    for j in range(16, 68):
        x = p1(w[j - 16] ^ w[j - 9] ^ Shift_left(w[j - 3], 15)) ^ Shift_left(w[j - 13], 7) ^ w[j - 6]
        w.append(x)
    for j in range(64):
        x = w[j] ^ w[j + 4]
        w2.append(x)
    # print("w1,w2",len(w),len(w2))
    # print("w1,w2",w,w2)
    A = cut_text(v, 8)
    # print("len(a),a",len(A),A)
    for i in range(8):
        A[i] = int(A[i], 16)
    for j in range(64):
        ss1 = Shift_left((Shift_left(A[0], 12) + A[4] + Shift_left(T(j), j)) % (2 ** 32), 7) % (2 ** 32)
        ss2 = (ss1 ^ Shift_left(A[0], 12)) % (2 ** 32)
        tt1 = (FF(A[0], A[1], A[2], j) + A[3] + ss2 + w2[j]) % (2 ** 32)
        tt2 = (GG(A[4], A[5], A[6], j) + A[7] + ss1 + w[j]) % (2 ** 32)
        A[3] = A[2]
        A[2] = Shift_left(A[1], 9)
        A[1] = A[0]
        A[0] = tt1
        A[7] = A[6]
        A[6] = Shift_left(A[5], 19)
        A[5] = A[4]
        A[4] = p0(tt2)

    a = ''
    for i in range(8):
        A[i] = str(hex(A[i])).split('0x')[1]
        k = 8 - len(A[i])
        a = a + k * '0' + A[i]
    v1 = int(a, 16) ^ int(v, 16)
    v1 = hex(v1).split('0x')[1]
    if len(v1) < 64:
        v1 = "0" * (64 - len(v1)) + str(v1)
    # print(v1,"v1")
    return v1


# 为了方便碰撞攻击以及测试，化简掉转化为acill码部分，选用16进制数
def G_hash(P):
    # 对明文 hash
    iv = '7380166f4914b2b9172442d7da8a0600a96f30bc163138aae38dee4db0fb0e4e'
    P = HEX(P)
    B = s2m2b(P)
    for b in B:
        if b != '':
            iv = cf(iv, b)
    return iv


if __name__ == '__main__':
    iv = '7380166f4914b2b9172442d7da8a0600a96f30bc163138aae38dee4db0fb0e4e'

    plain = ASCII(input("请输入明文："))

    B = s2m2b(plain)
    for b in B:
        if b != '':
            iv = cf(iv, b)
    print(iv)
