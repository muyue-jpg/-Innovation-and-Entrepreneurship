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


def Sign(m, n, d, G, k):  
    R = Multiplication(k, G)
    r = R[0] % n
    e = int(hashlib.sha256(m.encode("utf-8")).hexdigest(),16)
    s = (ModReverse(k, n) * (e + d * r)) % n
    return (r, s)


# func5:验证签名 （r,s）of M with P
def Verify(m, n, r, s, G, P):
    e = int(hashlib.sha256(m.encode("utf-8")).hexdigest(),16)
    w = ModReverse(s, n)
    arr = Addition(Multiplication((e*w % n), G), Multiplication((r*w % n), P))  # (r',s'=e·wG+r·wP)
    if arr[0] % n == r:
        return True
    else:
        return False


#从签名反推公钥 s^-1(eG+rP)=R,(sR-eG)r^-1=P y^2=x^3+7
def Deduce_pubkey(signature,message,n,G,p):
    s=signature[1] 
    r=signature[0]
    r_re=ModReverse(r,n)
    e = int(hashlib.sha256(message.encode("utf-8")).hexdigest(),16)
    y2=(r**3+7)
    y=Cipolla(y2,p)
    #可能的第一个公钥
    R1=(r,y)
    sR=Multiplication(s,R1)
    eG=Multiplication(e,G)
    negeG=(eG[0],p-eG[1])
    P1=Multiplication(r_re,Addition(sR,negeG))

    #可能的第二个公钥
    R2=(r,p-y)
    sR_=Multiplication(s,R2)
    P2=Multiplication(r_re,Addition(sR_,negeG))

    print("公钥1:",Verify(message,n,signature[0],signature[1],G,P1),(P1[0],P1[1]))
    print("公钥2:",Verify(message,n,signature[0],signature[1],G,P2),(P2[0],P2[1]))



def Legendre(y,p): # 判断二次剩余
    return pow(y,(p - 1) // 2,p)
def mul(a,b,p,w):#定义一个虚部乘法
    return ((a[0]*b[0]+a[1]*b[1]*w)%p,(a[1]*b[0]+a[0]*b[1])%p)
def qpow(a,n,p,w):# 虚数的快速幂
    ans=(1,0)
    while(n):
        if (n&1):
            ans = mul(ans,a,p,w)
        a =mul(a,a,p,w)
        n >>= 1
    return ans
def Cipolla(y,p): #计算二次剩余
    assert Legendre(y,p) == 1
    a=0
    while(1):
        i=secrets.randbelow(p)
        if Legendre(pow(i,2)-y,p) == p-1:
            a=i
            break
    w=a*a-y
    x=qpow((a,1),(p+1)//2,p,w)
    return(x[0])



message="hello world"
#随机产生[1,n]的私钥
while(1):
    private_key=int(secrets.token_hex(32),16)
    if 1<=private_key<=n:
        break
#private_key=17224582935078344674852530359386077739442000688743525513969135973603426714803
print("私钥:",(private_key))
#生成公钥
public_key=Multiplication(private_key,G)
print("公钥:",((public_key[0]),(public_key[1])))
#Sign
while(1):
    k=secrets.randbelow(n)
    if k != 0:
        break
#print(k)
#k=99173047618213209279979135175711262101418889298299676052286745039066960550091
sig=Sign(message,n,private_key,G,k)
print("消息:",message,"\nhash:",hashlib.sha256(message.encode("utf-8")).hexdigest())
print("签名：",sig)
print("验证签名：",Verify(message,n,sig[0],sig[1],G,public_key))

#deduce pubkey
print("\n.....deduce pubkey from signature.....")
print("签名：",sig)
Deduce_pubkey(sig,message,n,G,p)






