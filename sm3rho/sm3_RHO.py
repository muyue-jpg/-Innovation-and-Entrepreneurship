import sm3
import random
import time

def hash(exm):  # 获取哈希值
    a = hex(random.randint(0, 2 ** (exm + 1) - 1))[2:]
    a_1 = sm3.G_hash(a)
    a_2 = sm3.G_hash(a_1)
    return a, a_1, a_2


def rho_method(digit, r, r_1, r_2):
    i = 1
    while r_1[:digit] != r_2[:digit]:
        i += 1
        r_1 = sm3.G_hash(r_1)
        r_2 = sm3.G_hash(sm3.G_hash(r_2))

    r_2 = r_1
    r_1 = r
    for j in range(i):
        if sm3.G_hash(r_1)[:digit] == sm3.G_hash(r_2)[:digit]:
            return sm3.G_hash(r_1)[:digit], r_1, r_2
        else:
            r_1 = sm3.G_hash(r_1)
            r_2 = sm3.G_hash(r_2)


if __name__ == '__main__':
    example = 8
    start = time.time()
    r, r_1, r_2 = hash(example)
    x, m1, m2 = rho_method(int(example / 4), r, r_1, r_2)
    end = time.time()
    time=end-start
    print("success！")
    print("message1:", m1)
    print("message2:", m2)
    print("两者哈希值的前{}bit相同，16进制表示为:{},时间为：{}s".format(example, x, time))
