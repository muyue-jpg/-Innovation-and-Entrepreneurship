#ECDSA-secp256k1
from random import random
import secrets
import hashlib

# Recommended Parameters secp256k1 y**2=x**3+7
# p=0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEFFFFFC2F #有限域的阶
# a=0
# b=7
# G=(0x79BE667EF9DCBBAC55A06295CE870B07029BFCDB2DCE28D959F2815B16F81798,0x483ADA7726A3C4655DA4FBFC0E1108A8FD17B448A68554199C47D08FFB10D4B8)#生成元（为了方便直接以这种形式写）
# n=0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141 #生成元的阶


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
def Addition(point1, point2,q):
    if point1 == 0 and point2 == 0: return 0
    elif point1 == 0: return point2
    elif point2 == 0: return point1
    if point1 == point2:
        n1 = (3 * pow(point1[0], 2) + a) % q
        n2 = (2 * point1[1]) % q
        if n1 % n2 != 0:
            n2_re = ModReverse(n2, q)
            y = (n1 * n2_re) % q
        else:
            y = (n1 // n2) % q  
    else:
        n1 = (point1[1] - point2[1])
        n2 = (point1[0] - point2[0])
        if n1 % n2 == 0:
            y = (n1 // n2) % q
        else:
            n2_re = ModReverse(n2, q)
            y = (n1 * n2_re) % q
    R = []
    Rx = ((y**2) - point1[0] - point2[0]) % q
    Ry = (y * (point1[0] - Rx) - point1[1]) % q
    R.append(Rx)
    R.append(Ry)
    return R

#func3：有限域乘法
def Multiplication(N, P, q):
    flag = 1 << 255
    Q=0
    for i in range(255):
        if 0 != N & flag:
            Q = Addition(Q,P,q)
        Q = Addition(Q,Q,q)
        flag >>= 1 
    if 0 != N & flag:
        Q = Addition(Q,P,q)
    return Q


def Sign(m, n, d, G, k,q):  #s=k^-1(e+dr)mod n
    R = Multiplication(k, G, q)
    r = R[0] % n
    e = int(hashlib.sha256(m.encode("utf-8")).hexdigest(),16)
    s = (ModReverse(k, n) * (e + d * r)) % n
    return (r, s)


# func5:验证签名 （r,s）of M with P
def Verify(m, n, r, s, G, P, q):
    e = int(hashlib.sha256(m.encode("utf-8")).hexdigest(),16)
    w = ModReverse(s,n)
    arr = Addition(Multiplication((e*w % n),G,q), Multiplication((r*w % n),P,q),q)  # (r',s'=e·wG+r·wP)
    if arr[0] % n == r:
        return True
    else:
        return False


def Generate_key(n,q):
    while(1):
        private_key=int(secrets.token_hex(32),16)
        if 1<=private_key<=n:
            break
    #private_key=0x64CA290259A8D3089474E79FF7D3BC2B11F83B9B77B133D98D4B3FABD8949511
    public_key=Multiplication(private_key,G,q)
    return {'private key':private_key,'public key':public_key}

def Generate_K(n):
    while(1):
        k=secrets.randbelow(n)
        if k != 0:
            break
    return k

#Leaking k leads to leaking of d
#s=k^-1(e+dr)mod n -> d=(sk-e)r^-1 mod n
def Leaking_k(k,signature,message):
    e = int(hashlib.sha256(message.encode("utf-8")).hexdigest(),16)
    s=(signature[1]*k-e) % n
    r_re=ModReverse(signature[0],n)
    d=r_re*s%n
    return d

##reusing k leads to leaking of d##
# s=k^-1(e+dr)mod n -> r= kG (r is same)->s1-s2=k^-1(e1-e2) mod n->k=(e1-e2)(s1-s2)^-1 mod n
def Reusing_k(message1,message2,sign1,sign2):
    e1=int(hashlib.sha256(message1.encode("utf-8")).hexdigest(),16)
    e2=int(hashlib.sha256(message2.encode("utf-8")).hexdigest(),16)
    k=(e1-e2)*(ModReverse(sign1[1]-sign2[1],n)) % n
    return k



if __name__=="__main__":
    # Recommended Parameters secp256k1 y**2=x**3+7
    # p=0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEFFFFFC2F #有限域的阶
    # a=0
    # b=7
    # G=(0x79BE667EF9DCBBAC55A06295CE870B07029BFCDB2DCE28D959F2815B16F81798,0x483ADA7726A3C4655DA4FBFC0E1108A8FD17B448A68554199C47D08FFB10D4B8)#生成元（为了方便直接以这种形式写）
    # n=0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141 #生成元的阶

    #sm2
    p=0xFFFFFFFEFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF00000000FFFFFFFFFFFFFFFF
    a=0xFFFFFFFEFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF00000000FFFFFFFFFFFFFFFC
    b=0x28E9FA9E9D9F5E344D5A9E4BCF6509A7F39789F515AB8F92DDBCBD414D940E93
    n=0xFFFFFFFEFFFFFFFFFFFFFFFFFFFFFFFF7203DF6B21C6052B53BBF40939D54123
    xG=0x32C4AE2C1F1981195F9904466A39C9948FE30BBFF2660BE1715A4589334C74C7
    yG=0xBC3736A2F4F6779C59BDCEE36B692153D0A9877CC62A474002DF32E52139F0A0
    G=(xG,yG)
    message="hello world"
    #随机产生[1,n]的私钥
    #private_key=17224582935078344674852530359386077739442000688743525513969135973603426714803
    Key=Generate_key(n,p)
    print("私钥:",hex(Key["private key"])[2:])
    #生成公钥
    #public_key=Multiplication(private_key,G)
    print("公钥:",(hex(Key['public key'][0])[2:],hex(Key['public key'][1])[2:]))
    Sign
    k=Generate_K(n)
    #print(k)
    #k=99173047618213209279979135175711262101418889298299676052286745039066960550091
    #k=0x6C47464183BB16B66BBB50BD1C48184697DDACCC24D1D65C58D6E294079C5A92
    sig=Sign(message,n,Key["private key"],G,k,p)
    print("消息:",message,"\nhash:",hashlib.sha256(message.encode("utf-8")).hexdigest())
    print("签名：",sig)
    print("验证签名：",Verify(message,n,sig[0],sig[1],G,Key["public key"],p))

##leaking k
    # print("\n....leaking k leads to leaking of d....")
    # d=Leaking_k(k,sig,message)
    # print("k:",k)
    # print('original private key:',Key['private key'])
    # print('computed private key:',d)

##reusing k
    # print("\n....reusing k leads to leaking of d....")
    # message2='bye bye'
    # sig2=Sign(message2,n,Key['private key'],G,k,p)
    # k_=Reusing_k(message,message2,sig,sig2)
    # print("original k:",k)
    # print("computed k_:",k_)
    # print("//then use k_ to compute private key//")
    # key=Leaking_k(k_,sig,message)
    # print("original private key:",Key['private key'])
    # print("computed private key:",key)

##Two users, using k leads to leaking of d, that is they can deduce each other's d
# 因为泄露k会导致泄露私钥，如果两个用户使用一样的k，其中一个用户便能用自己的k计算出另一个人的私钥
# ECDSA比sm2签名简单，所以本质和泄露k是一样的
    # messageA='wakuwaku'
    # KeyA=Generate_key(n,p)
    # kA=Generate_K(n)
    # sigA=Sign(messageA,n,KeyA['private key'],G,kA,p)
    # Alice={ 'message':messageA,
    #         'private key':KeyA['private key'],
    #         'K':kA,
    #         'signature':sigA}

    # messageB='byebyebye'
    # KeyB=Generate_key(n,p)
    # kB=kA
    # sigB=Sign(messageB,n,KeyB['private key'],G,kB,p)
    # Bob={   'message':messageB,
    #         'private key':KeyB['private key'],
    #         'K':kB,
    #         'signature':sigB}

    # print("//Alice can compute Bob 's private key//")
    # dB_=Leaking_k(kA,Bob['signature'],Bob['message'])
    # print("Bob 's private key:",Bob['private key'])
    # print("computed key by Alice with the same k:",dB_)

    # print("//Bob can compute Alice 's private key//")
    # dA_=Leaking_k(kB,Alice['signature'],Alice['message'])
    # print("Alice 's private key:",Alice['private key'])
    # print("computed key by Bob with the same k:",dA_)

