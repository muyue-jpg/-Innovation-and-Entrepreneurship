import binascii
import re
from math import ceil

IV = [
    1937774191, 1226093241, 388252375, 3666478592,
    2842636476, 372324522, 3817729613, 2969243214,
]


def T(j):
    if j < 16:
        T = int('0x79cc4519', 16)
    if 15 < j < 64:
        T = int('0x7a879d8a', 16)
    return T


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


def sm3_cf(v_i, b_i):
    w = []
    for i in range(16):
        weight = 0x1000000
        data = 0
        for k in range(i * 4, (i + 1) * 4):
            data = data + b_i[k] * weight
            weight = int(weight / 0x100)
        w.append(data)

    for j in range(16, 68):
        w.append(0)
        w[j] = p1(w[j - 16] ^ w[j - 9] ^ Shift_left(w[j - 3], 15)) ^ Shift_left(w[j - 13], 7) ^ w[j - 6]

    w_1 = []
    for j in range(0, 64):
        w_1.append(0)
        w_1[j] = w[j] ^ w[j + 4]

    a, b, c, d, e, f, g, h = v_i

    for j in range(0, 64):
        ss1 = Shift_left((Shift_left(a, 12) + e + Shift_left(T(j), j)) % (2 ** 32), 7) % (2 ** 32)
        ss2 = (ss1 ^ Shift_left(a, 12)) % (2 ** 32)
        tt_1 = (FF(a, b, c, j) + d + ss2 + w_1[j]) % (2 ** 32)
        tt_2 = (GG(e, f, g, j) + h + ss1 + w[j]) % (2 ** 32)
        d = c
        c = Shift_left(b, 9)
        b = a
        a = tt_1
        h = g
        g = Shift_left(f, 19)
        f = e
        e = p0(tt_2)

        a, b, c, d, e, f, g, h = map(
            lambda x: x & 0xFFFFFFFF, [a, b, c, d, e, f, g, h])

    v_j = [a, b, c, d, e, f, g, h]
    return [v_j[i] ^ v_i[i] for i in range(8)]


def sm3_hash(msg, new_v):
    # print(msg)
    len1 = len(msg)
    reserve1 = len1 % 64
    msg.append(0x80)
    reserve1 = reserve1 + 1
    # 56-64, add 64 byte
    range_end = 56
    if reserve1 > range_end:
        range_end = range_end + 64

    for i in range(reserve1, range_end):
        msg.append(0x00)

    bit_length = (len1) * 8
    bit_length_str = [bit_length % 0x100]
    for i in range(7):
        bit_length = int(bit_length / 0x100)
        bit_length_str.append(bit_length % 0x100)
    for i in range(8):
        msg.append(bit_length_str[7 - i])

    group_count = round(len(msg) / 64) - 1

    B = []
    for i in range(0, group_count):
        B.append(msg[(i + 1) * 64:(i + 2) * 64])

    V = []
    V.append(new_v)
    for i in range(0, group_count):
        V.append(sm3_cf(V[i], B[i]))

    y = V[i + 1]
    result = ""
    for i in y:
        result = '%s%08x' % (result, i)
    return result


def sm3_kdf(z, klen):  # z为16进制表示的比特串（str），klen为密钥长度（单位byte）
    klen = int(klen)
    ct = 0x00000001
    rcnt = ceil(klen / 32)
    Z = [i for i in bytes.fromhex(z.decode('utf8'))]
    ha = ""
    for i in range(rcnt):
        msg = Z + [i for i in binascii.a2b_hex(('%08x' % ct).encode('utf8'))]
        ha = ha + sm3_hash(msg)
        ct += 1
    return ha[0: klen * 2]
