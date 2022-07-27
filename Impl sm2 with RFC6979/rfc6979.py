#实现基于sm3的hmac和用rfc4979生成sm2需要的k值
import sm3
import math
## 整数x转换到k字节的字节串
def int2byte(x,k)->str:#k:目标字节串的长度
    if(2**(8*k)<=x):
        print("int2byte Error!x is too big!")
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

#域上数转换为字节串
def f2byte(a:int,p:int)->str:
    t=math.ceil(math.log2(p))   
    l=math.ceil(t/8)
    return int2byte(a,l)

def sm3hash(message)->str:
    iv = '7380166f4914b2b9172442d7da8a0600a96f30bc163138aae38dee4db0fb0e4e'
    plain = byte2bit(message)
    B = sm3.s2m2b(plain)
    for b in B:
        if b != '':
            iv = sm3.cf(iv, b)
    return(int2byte(int(iv,16),32))

def hmac_sm3(message:str,K:str):
    text=''
    for i in message:
        text=text+str(hex(ord(i))[2:])
    while(len(K)<2*64):
            K=K+'0'
    if (len(K)>2*64):
        K=sm3hash(K)
    ipad='36'*64
    opad='5C'*64
    h1=sm3hash(int2byte(byte2int(K)^byte2int(ipad),64)+text)
    h2=sm3hash(int2byte(byte2int(K)^byte2int(opad),64)+h1)
    return h2

def rfc6979_sm2(message:str,private_key:int,p:int):
    m=''
    for i in message:
        m=m+str(hex(ord(i))[2:])
    h1=sm3hash(m)
    V='01'*32#Vlen=8*ceil(hlen/8),hlen=256(to sm3)
    K='00'*32#Klen=8*ceil(hlen/8),hlen=256(to sm3)
    K=hmac_sm3(V+'00'+f2byte(private_key,p)+h1,K)
    V=hmac_sm3(V,K)
    K=hmac_sm3(V+'01'+f2byte(private_key,p)+h1,K)
    V=hmac_sm3(V,K)
    qlen=math.ceil(math.log2(p))
    T=''
    tlen=len(T)
    while(tlen < qlen//4):
        V=hmac_sm3(V,K)
        #print(len(V),tlen)
        T=T+V
        tlen=len(T)
    k=byte2int(T)
    while(1):
        if (1<=k<=p-1):
            return k
        K=hmac_sm3(V+'00',K)
        V=hmac_sm3(V,K)
        T=''
        tlen=len(T)
        while(tlen < qlen//4):
            V=hmac_sm3(V,K)
            T=T+V
        k=byte2int(T)



