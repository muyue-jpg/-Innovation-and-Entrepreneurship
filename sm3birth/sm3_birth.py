import sm3
import time

def birth_atk(exm):
    Primal_space = int(2 ** (exm / 2))  # 搜索空间大小
    ans = [0] * 2**exm
    for i in range(Primal_space):
        temp = int(sm3.G_hash(str(i))[0:int(exm / 4)], 16)
        if ans[temp] == 0:
            ans[temp] = i
        else:
            return hex(temp), i, ans[temp]


if __name__ == '__main__':

    example = 24
    start=time.time()
    a, m_1, m_2 = birth_atk(example)
    end=time.time()
    time=end-start
    print("success! 找到碰撞，消息{}与{}哈希值的前{}bit相同，16进制表示为:{},所花费时间为:{} 。".format(m_1, m_2, example, a, time))
