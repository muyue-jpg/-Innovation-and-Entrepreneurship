#实现了基于sm3和使用sm2推荐参数的ECMH
import sm3
from random import random
import secrets
import math
#recommended parameters 
p=0xFFFFFFFEFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF00000000FFFFFFFFFFFFFFFF
a=0xFFFFFFFEFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF00000000FFFFFFFFFFFFFFFC
b=0x28E9FA9E9D9F5E344D5A9E4BCF6509A7F39789F515AB8F92DDBCBD414D940E93
n=0xFFFFFFFEFFFFFFFFFFFFFFFFFFFFFFFF7203DF6B21C6052B53BBF40939D54123
xG=0x32C4AE2C1F1981195F9904466A39C9948FE30BBFF2660BE1715A4589334C74C7
yG=0xBC3736A2F4F6779C59BDCEE36B692153D0A9877CC62A474002DF32E52139F0A0
G=(xG,yG)
#test parameters
# p=0x8542D69E4C044F18E8B92435BF6FF7DE457283915C45517D722EDB8B08F1DFC3
# a=0x787968B4FA32C3FD2417842E73BBFEFF2F3C848B6831D7E0EC65228B3937E498
# b=0x63E4C6D3B23B0C849CF84241484BFE48F61D59A5B16BA06E6E12D1DA27C5249A
# n=0x8542D69E4C044F18E8B92435BF6FF7DD297720630485628D5AE74EE7C32E79B7
# xG=0x421DEBD61B62EAB6746434EBC3CC315E32220B3BADD50BDC4C4E6C147FEDD43D
# yG=0x0680512BCBB42C07D47349D2153B70C4E5D7FDFCBFA36EA1A85841B9E46E09A2
# G=(xG,yG)


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

#求解二次剩余
def Legendre(n,p): # 判断二次剩余
    return pow(n,(p - 1) // 2,p)
def mul(a,b,p,w):#定义一个虚数乘法
    return ((a[0]*b[0]+a[1]*b[1]*w)%p,(a[1]*b[0]+a[0]*b[1])%p)
def qpow(a,n,p,w):# 虚数的快速幂
    ans=(1,0)
    while(n):
        if (n&1):
            ans = mul(ans,a,p,w)
        a =mul(a,a,p,w)
        n >>= 1
    return ans
def Cipolla(n,p): #Cipolla算法
    if(Legendre(n,p) != 1):#"n is not quadratic residue"
        return False
    a=0
    while(1):
        i=secrets.randbelow(p)
        if Legendre(pow(i,2)-n,p) == p-1:
            a=i
            break
    w=a*a-n
    x=qpow((a,1),(p+1)//2,p,w)
    return(x[0])
    
def sm3hash(message)->str:
    iv = '7380166f4914b2b9172442d7da8a0600a96f30bc163138aae38dee4db0fb0e4e'
    plain = byte2bit(message)
    B = sm3.s2m2b(plain)
    for b in B:
        if b != '':
            iv = sm3.cf(iv, b)
    return(int2byte(int(iv,16),32))

## 整数x转换到k字节的字节串
def int2byte(x,k)->str:#x:bit length,k:目标字节串的长度
    if(2**(8*k)<=x):
        print("int2byte Error!")
        exit()
    x_hex=hex(x).upper()[2:]
    while(len(x_hex)<2*k):
        x_hex='0'+x_hex
    return x_hex

## M字节串转换bit串
def byte2bit(M)->str:
    k=len(M)//2
    s=bin(int(M,16))[2:]
    while(len(s)<8*k):
        s="0"+s
    return s

#字节串转换为整数
def byte2int(M)->int:
    for i in range(len(M)):
        if M[i]!= '0':
            M=M[i:]
            break
    return int(M,16)

#域元素到字节串
def f2byte(a)->str:
    t=math.ceil(math.log2(p))   
    l=math.ceil(t/8)
    return int2byte(a,l)

#ECMH
def ecmh(U:set)->int:
    sum_set=0
    for i in range(len(U)):
        h1=sm3hash(U[i])
        j=0
        val=hex(j)[2:]+h1
        h2=sm3hash(val)
        X=(pow(byte2int(h2),3,p)+a*byte2int(h2)+b) % p
        while(Legendre(X,p)!=1):
            j=j+1
            val=hex(j)[2:]+h1
            h2=sm3hash(val)
            X=(pow(byte2int(h2),3,p)+a*byte2int(h2)+b) % p
        y=Cipolla(X,p)
        if (p-y<=y):
            y=p-y
        point=(byte2int(h2),y)
        sum_set=Addition(sum_set,point)

    return (sum_set[0])

def plus(h1,h2):
    Y1=h1**3+a*h1+b % p
    y1=Cipolla(Y1,p)
    if (p-y1<=y1):
        y1=p-y1
    Y2=h2**3+a*h2+b % p
    y2=Cipolla(Y2,p)
    if (p-y2<=y2):
        y2=p-y2
    sum=Addition((h1,y1),(h2,y2))
    return sum[0]

def minus(h1,h2):
    Y1=h1**3+a*h1+b % p
    y1=Cipolla(Y1,p)
    if (p-y1<=y1):
        y1=p-y1
    Y2=h2**3+a*h2+b % p
    y2=Cipolla(Y2,p)
    if (p-y2<=y2):
        y2=p-y2
    sub=Addition((h1,y1),(h2,p-y2))
    return sub[0]
        
if __name__=="__main__":
    m1="Alice_i_love_you".encode('utf-8').hex()
    m2='Bob_i_love_you_too'.encode('utf-8').hex()
    h1=ecmh((m1,))
    h2=ecmh((m2,))
    h3=ecmh((m1,m2))
    h4=ecmh((m2,m1))
    print("{m1}:",(m1,),"\nhash:",f2byte(h1))
    print("{m2}:",(m2,),"\nhash:",f2byte(h2))
    print("{m1,m2}:",(m1,m2),"\nhash:",f2byte(h3))
    print("{m2,m1}:",(m2,m1),"\nhash:",f2byte(h4))
    print("H({m1})+H({m2})=",f2byte(plus(h1,h2)))
    print("H({m2})+H({m1})=",f2byte(plus(h2,h1)))

    print("H({m1+m2})-H({m1})=",f2byte(minus(h3,h1)))



