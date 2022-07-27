Same d and k with ECDSA, leads to leaking of d

sm2:

![](1.png)

ecdsa:

![](2.png)

由这两个签名和ecdsa消息的hash可以计算出私钥d

![](3.png)