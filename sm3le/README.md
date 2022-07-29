
Project: implement length extension attack for SM3, SHA256, etc.

进行长度拓展攻击，使用python的sm3库函数sm3.hash函数进行测试，同时做略微修改，增加一个new_v输入

攻击过程为：

1.random随机生成一个secret，用sm3_hash函数算出secret的hash值

2.生成附加信息m

3.根据hash值推出第一次压缩之后8个向量的值

4.在secret+padding之后附加一段消息，用上一步向量的值作为初始值IV去加密附加的那段消息，得到hash

5.用sm3去加密secret+padding+m'，得到hash

6.如果攻击成功，第4步和第5 步得到的hash值应该相等

pedding()：用于填充消息

hash():伪造信息

attack():进行攻击

生成随机secret：

![image](https://user-images.githubusercontent.com/66394822/181144029-f056307c-7ad3-473d-b969-640ae2430799.png)

附加信息的hash值：

![image](https://user-images.githubusercontent.com/66394822/181144063-b488ab83-3a4b-4a49-9007-7041c406e3f8.png)

调用attack函数进行攻击并验证结果：

![image](https://user-images.githubusercontent.com/66394822/181144087-4dabb73a-0810-4ae8-8267-b20df6dd1737.png)
