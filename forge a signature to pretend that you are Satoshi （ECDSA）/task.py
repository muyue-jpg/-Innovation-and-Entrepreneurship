#ECDSA-secp256k1
from random import random
import secrets
import hashlib

# Recommended Parameters secp256k1 y**2=x**3+7
p=0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEFFFFFC2F #有限域的阶
a=0
b=7
G=(0x79BE667EF9DCBBAC55A06295CE870B07029BFCDB2DCE28D959F2815B16F81798,0x483ADA7726A3C4655DA4FBFC0E1108A8FD17B448A68554199C47D08FFB10D4B8)#生成元（为了方便直接以这种形式写）
n=0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141 #生成元的阶

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
def Addition(point1, point2):
    if point1 == 0 and point2 == 0: return 0
    elif point1 == 0: return point2
    elif point2 == 0: return point1
    if point1 == point2:
        n1 = (3 * pow(point1[0], 2) + a) % p
        n2 = (2 * point1[1]) % p
        if n1 % n2 != 0:
            n2_re = ModReverse(n2, p)
            y = (n1 * n2_re) % p
        else:
            y = (n1 // n2) % p   
    else:
        n1 = (point1[1] - point2[1])
        n2 = (point1[0] - point2[0])
        if n1 % n2 == 0:
            y = (n1 // n2) % p
        else:
            n2_re = ModReverse(n2, p)
            y = (n1 * n2_re) % p
    R = []
    Rx = ((y**2) - point1[0] - point2[0]) % p
    Ry = (y * (point1[0] - Rx) - point1[1]) % p
    R.append(Rx)
    R.append(Ry)
    return R


#func3：有限域乘法
def Multiplication(N, P):
    flag = 1 << 255
    Q=0
    for i in range(255):
        if 0 != N & flag:
            Q = Addition(Q,P)
        Q = Addition(Q,Q)
        flag >>= 1 
    if 0 != N & flag:
        Q = Addition(Q,P)
    return Q


# func5:验证签名 （r,s）of M with P
def Verify_only_hash(e, n, r, s, G, P):
    w = ModReverse(s, n)
    arr = Addition(Multiplication((e*w % n), G), Multiplication((r*w % n), P))  # (r',s'=e·wG+r·wP)
    if arr[0] % n == r:
        return True
    else:
        return False


#forge signature

public_key=(0xae1a62fe09c5f51b13905f07f06b99a2f7159b2225f374cd378d71302fa28414,0xe7aab37397f554a7df5f142c21c1b7303b8a0626f1baded5c72a704f7e6cd84c)
u=secrets.randbelow(n)
v=secrets.randbelow(n)
R_=Addition(Multiplication(u,G),Multiplication(v,public_key))
r_=R_[0]%n
s_=r_*ModReverse(v,n)%n
e_=r_*u*ModReverse(v,n)%n
print('only check hash in ecdsa sign verify')
print('forged r:{}\nforged s:{}\nforged e:{}'.format(r_,s_,e_))
print(Verify_only_hash(e_,n,r_,s_,G,public_key))







