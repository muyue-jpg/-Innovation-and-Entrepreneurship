*Project: Impl Merkle Tree following RFC6962
• Construct a Merkle tree with 10w leaf nodes
• Build inclusion proof for specified element
• Build exclusion proof for specified element

1.在代码中Node类定义了叶节点

2.MerkleTree类定义了merkletree及一系列操作，包括创建merkle树，获取根节点的哈希值，为指定元素建立包含证明

3.然后开始构建具有100000叶节点的Merkle树

4.检查是否包含特定元素

这里代码参考了https://github.com/azranohad/merkel_tree 提供的merkletree代码，万般感谢


运行截图如下


![BC9TX9`Z8R%83WP9 (~J9_B](https://user-images.githubusercontent.com/80380151/181731789-9f82dc43-36ef-4592-ba80-8e691019b491.png)
