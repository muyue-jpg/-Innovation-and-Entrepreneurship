
Project: implement the naïve birthday attack of reduced SM3

通过概率论进行比特碰撞进行攻击。

sm3.py为根据国家文档所写出算法，并加入了将字符串通过ACILL码变为二进制数，但在测试中，为了方便观察，仅使用16进制的输入。

birth_atk（）：传入的exm为找到碰撞信息的前exm比特数相同

Primal_space：搜索空间大小

ans[]：存储hash信息

如果hash值对应的数组位置为空，进行存储；如果hash值对应数组位置不为空则找到碰撞，返回结果，最高实现了31bit的碰撞

![image](https://user-images.githubusercontent.com/66394822/181137672-a69686b7-f29c-44df-a5ec-c4f6b9d32485.png)
