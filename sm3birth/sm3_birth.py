import sm3
import time


def birth_atk(exm):
    Primal_space = int(pow(2, exm / 2))  # 搜索空间大小
    ans = [0] * pow(2, exm)
    for i in range(Primal_space):
        temp = int(sm3.G_hash(str(i))[0:int(exm / 4)], 16)
        if ans[temp] == 0:
            ans[temp] = i
        else:
            return hex(temp), i, ans[temp]


if __name__ == '__main__':
    example = 24
    start = time.time()
    a, m_1, m_2 = birth_atk(example)
    end = time.time()
    time = end - start
    print("碰撞成功")
    print("消息:", m_1, "和消息:", m_2, "的hash值的前", example, "比特相同")
    print("16进制表示:", a, "time:", time)
