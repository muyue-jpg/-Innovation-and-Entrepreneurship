#实现了Fp上的sm2
import sys
import os
path=os.path.abspath('')
sys.path.append(path)
import sm3
from random import random
import secrets
import hashlib
import math
import rfc6979
from ECDSA import task as ecdsa

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


# func2:椭圆曲线加法
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


#func3：椭圆曲线乘法
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


def Generate_ZA(ENTLA,IDA,a,b,xG,yG,xA,yA)->str:
    Z=ENTLA+IDA+f2byte(a)+f2byte(b)+f2byte(xG)+f2byte(yG)+f2byte(xA)+f2byte(yA)
    return sm3hash(Z)

def Generate_key():
    while(1):
        private_key=int(secrets.token_hex(32),16)
        if 1<=private_key<=n-2:
            break
    #test key
    #private_key=byte2int("128B2FA8BD433C6C068C8D803DFF79792A519A55171B1B650C23661D15897263")
    #private_key=0x64CA290259A8D3089474E79FF7D3BC2B11F83B9B77B133D98D4B3FABD8949511
    public_key=Multiplication(private_key,G)
    return {'private key':private_key,'public key':public_key}

def Generate_K():
    while(1):
        k=secrets.randbelow(n)
        if k != 0:
            break
    return k

def Generate_IDA(id):
    IDA=''
    for i in id:
        IDA=IDA+str(hex(ord(i)).upper()[2:])
    return IDA

def print_byte(a):
    count=0
    s=''
    for i in a:
        count=count+1
        s=s+i
        if count%8==0:
            s=s+' '
    return s

#sm2签名算法
def sm2_sign(ZA,message,dA)->str:
    M=''
    for i in message:
        M=M+str(hex(ord(i))[2:])
    M_=ZA+M
    e=byte2int(sm3hash(M_))
    while(1):
        #k=Generate_K()
        k=rfc6979.rfc6979_sm2(message,dA,p)
        print('k:{{\n {k}\n}}'.format(k=print_byte(f2byte(k))))
        #test k
        #k=0x6cb28d99385c175c94f94e934817663fc176d925dd72b727260dbaae1fb2f96f
        #k=0x6C47464183BB16B66BBB50BD1C48184697DDACCC24D1D65C58D6E294079C5A92
        kG=Multiplication(k,G)
        r=(e+kG[0])%n
        if(r==0 or r+k==n):
            continue
        s=(ModReverse(1+dA,n)*(k-r*dA))%n
        if(s==0):
            continue
        break
    return (f2byte(r),f2byte(s))

#sm2签名验证算法
def sm2_sign_verify(message,sig,PA,ZA):
    r_=byte2int(sig[0])
    s_=byte2int(sig[1])
    if not 1<=r_<=n-1:
        return False
    if not 1<=s_<=n-1:
        return False
    M=''
    for i in message:
        M=M+str(hex(ord(i))[2:])
    M_=ZA+M
    e_=byte2int(sm3hash(M_))
    t=(r_+s_)%n
    if t==0:
        return False
    X=Addition(Multiplication(s_,G),Multiplication(t,PA))
    R=(e_+X[0])%n
    if R!=r_:
        return False
    else:
        return True
#m="F4A38489E32B45B6F876E3AC2168CA392362DC8F23459C1D1146FC3DBFB7BC9A6D65737361676520646967657374"
if __name__=="__main__":
    #recommended parameters 
    p=0xFFFFFFFEFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF00000000FFFFFFFFFFFFFFFF
    a=0xFFFFFFFEFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF00000000FFFFFFFFFFFFFFFC
    b=0x28E9FA9E9D9F5E344D5A9E4BCF6509A7F39789F515AB8F92DDBCBD414D940E93
    n=0xFFFFFFFEFFFFFFFFFFFFFFFFFFFFFFFF7203DF6B21C6052B53BBF40939D54123
    xG=0x32C4AE2C1F1981195F9904466A39C9948FE30BBFF2660BE1715A4589334C74C7
    yG=0xBC3736A2F4F6779C59BDCEE36B692153D0A9877CC62A474002DF32E52139F0A0
    G=(xG,yG)

##sign
    print('-------sign--------')
    id="Alice_i_love_you_three_thousand_years"
    #IDA简单的取id的acsii码的16进制表示
    IDA=Generate_IDA(id)
    #test IDA
    #IDA="414c494345313233405941484f4f2e434f4d"
    print("IDA:",print_byte(IDA))
    #IDA的bit长度的两字节形式
    ENTLA=int2byte(len(byte2bit(IDA)),2)
    KEY=Generate_key()
    ZA=Generate_ZA(ENTLA,IDA,a,b,xG,yG,KEY['public key'][0],KEY['public key'][1])
    #print(ZA)
    message='hello hello'
    #test message
    #message='message digest'
    print('message:',message)
    print("private key:{\n",print_byte(f2byte(KEY['private key'])),'\n}')
    print("public key:{{\n x:{x}\n y:{y}\n}}".format(x=print_byte(f2byte(KEY['public key'][0])),y=print_byte(f2byte(KEY['public key'][1]))))
    sig=sm2_sign(ZA,message,KEY['private key'])
    print("signature:{{\n r:{r}\n s:{s}\n}}".format(r=print_byte(sig[0]),s=print_byte(sig[1])))
    print('---------------------------------')

##verify sign###
    # print("verify the signature:\nZA:{za}\nmessage:{m}\nsignature:\nr:{r}\ns:{s}\nverify:{V}".format(za=print_byte(ZA),m=message,r=print_byte(sig[0]),s=print_byte(sig[1]),V=sm2_sign_verify(message,sig,KEY['public key'],ZA)))
    # print('--------different ZA---------------------')
    # id_="Bob_test_test_forever"
    # IDA_=Generate_IDA(id_)
    # ENTLA_=int2byte(len(byte2bit(IDA_)),2)
    # ZA_=Generate_ZA(ENTLA_,IDA_,a,b,xG,yG,KEY['public key'][0],KEY['public key'][1])
    # print("verify the signature:\nZA:{za}\nmessage:{m}\nsignature:\nr:{r}\ns:{s}\nverify:{V}".format(za=print_byte(ZA_),m=message,r=print_byte(sig[0]),s=print_byte(sig[1]),V=sm2_sign_verify(message,sig,KEY['public key'],ZA_)))

#Same d and k with ECDSA, leads to leaking of d
    # print('Same d and k with ECDSA, leads to leaking of d...')
    # sig2=(byte2int(sig[0]),byte2int(sig[1]))
    # sig1=(68191553287468095656764210092355924919030978489780542705082430394142805169685, 66836246292651079092568568747894603363024933544589514212317723500488999453541)
    # e1=0xb94d27b9934d3e08a52e52d7da7dabfac484efe37a5380ee9088f7ace2efcde9
    # d=(sig1[1]*sig2[1]-e1)*ModReverse((sig1[0]-sig1[1]*sig2[1]-sig1[1]*sig2[0]),n)%n
    # print(hex(d)[2:])