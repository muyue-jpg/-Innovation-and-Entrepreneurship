Project: implement length extension attack for SM3, SHA256, etc.

对sha256进行长度拓展攻击

攻击过程为：

1.使用预共享密钥生成消息

2.消息和签名通过网络传输，攻击者不知道预共享秘钥

3.攻击者获取并手动计算填充附加到消息中

4.攻击者将任意文本添加到消息中，重新hash并转发，替换原消息

5.此时消息 + 签名已到达目的地，因此我们可以再次使用预共享密钥。

6.服务器简单检查 sha256（PSK + 消息）是否与签名匹配。如果是这样，它接受签名，因为它认为它受PSK保护。



运行结果如下所示

![J _OL9R)9R)ZBF%`0V8}LLM](https://user-images.githubusercontent.com/80380151/181707316-c4873eab-7b4b-4bf1-a666-559be0f7db42.png)
