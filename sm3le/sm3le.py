from gmssl import sm3, func
import random
import my_sm3
import struct

def padding(msg):
    mlen = len(msg)
    msg.append(0x80)
    mlen += 1
    tail = mlen % 64
    range_end = 56
    if tail > range_end:
        range_end = range_end + 64
    for i in range(tail, range_end):
        msg.append(0x00)
    bit_len = (mlen - 1) * 8
    msg.extend([int(x) for x in struct.pack('>q', bit_len)])
    for j in range(int((mlen - 1) / 64) * 64 + (mlen - 1) % 64, len(msg)):
        global pad
        pad.append(msg[j])
        global pad_str
        pad_str += str(hex(msg[j]))
    return msg


def hash(old_hash, secret_len, append_m):
    vectors = []
    message = ""
    # 将old_hash分组，每组8个字节, 并转换为整数
    for r in range(0, len(old_hash), 8):
        vectors.append(int(old_hash[r:r + 8], 16))

    # 伪造消息
    if secret_len > 64:
        for i in range(0, int(secret_len / 64) * 64):
            message += '0'
    for i in range(0, secret_len % 64):
        message += '0'
    message = func.bytes_to_list(bytes(message, encoding='utf-8'))
    message = padding(message)
    message.extend(func.bytes_to_list(bytes(append_m, encoding='utf-8')))
    return my_sm3.sm3_hash(message, vectors)




def attack(n1, n2, n3):  # attack(secret, append_m, secret_hash)
    guess_hash = hash(n3, len(n1), n2)
    new_msg = func.bytes_to_list(bytes(n1, encoding='utf-8'))
    new_msg.extend(pad)
    new_msg.extend(func.bytes_to_list(bytes(n2, encoding='utf-8')))
    new_msg_str = n1 + pad_str + n2
    new_hash = sm3.sm3_hash(new_msg)
    return guess_hash, new_msg_str, new_hash


if __name__ == '__main__':
    secret = str(random.random())
    secret_hash = sm3.sm3_hash(func.bytes_to_list(bytes(secret, encoding='utf-8')))
    append_m = input("请输入：")  # 附加消息
    pad_str = ""
    pad = []

    guess_hash, new_msg_str, new_hash = attack(secret, append_m, secret_hash)
    print("生成secrect")
    print("secret: " + secret)
    print("secret length:%d" % len(secret))
    print("secret hash:" + secret_hash)
    print("附加消息:", append_m)
    print("人为构造的消息的hash值")
    print("hash_guess:" + guess_hash)
    print("验证攻击是否成功")
    print("计算hash(secret+padding+append_m')")
    print("new message: \n" + new_msg_str)
    print("hash(new message):" + new_hash)
    if new_hash == guess_hash:
        print("success!")
    else:
        print("fail..")
