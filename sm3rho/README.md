
Project: implement the Rho method of reduced SM3

rho_method():rho实现方法，digit为位数，不断构造p环

随机生成两个hash值，构造循环直到两者的hash值前digit比特位相同，则输出结果

攻击结果如下：
![image](https://user-images.githubusercontent.com/66394822/181147694-d25c6b2a-c09b-47bd-ac36-09454f00bce5.png)

