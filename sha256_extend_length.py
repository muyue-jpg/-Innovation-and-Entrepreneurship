from sha256 import SHA256, _pad
import random, string

PRE_SHARED_KEY = ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(20))

def generate_sig(message):
    plaintext = (PRE_SHARED_KEY + message).encode('utf-8')
    hash_algo = SHA256()
    hash_algo.update(plaintext)
    signature = hash_algo.hexdigest()
    print(f"消息签名为: {signature}\n")
    return signature

def transfer_sig(message, signature, psk_len):

    HASH_LEN = 32 * 2 #2 hex chars = 1 byte
    REG_SIZE = 4 * 2 #2 hex chars = 1 byte

    registers = []
    for i in range(0, HASH_LEN, REG_SIZE):
        hex_string = signature[i : i + REG_SIZE]
        registers.append(int(hex_string, 16))

    print("攻击者得到的值:")
    print("\t" + ",".join([hex(x) for x in registers]))

    #计算并手动将填充预先附加到我们的消息中
    padding = _pad(len(message) + psk_len)

    #将任意文本添加到我们的消息中，重新哈希，然后将其转发
    attacker_message = "experience as your reference, prudence as your brother and hope as your sentry"
    malicious_hasher = SHA256()

    #替换
    malicious_hasher._h = registers
    malicious_hasher._counter = psk_len + len(message) + len(padding)


    malicious_hasher.update(attacker_message.encode('utf-8'))

    #替换
    attacker_message = message.encode('utf-8') + padding + attacker_message.encode('utf-8')
    signature = malicious_hasher.hexdigest()

    return attacker_message, signature

#检查哈希值与签名是否匹配
def submit(message, sig):
    hashing_algo = SHA256()
    hashing_algo.update(PRE_SHARED_KEY.encode("utf-8") + message)
    calculated_signature = hashing_algo.hexdigest()
    return (sig == calculated_signature)


MESSAGE = "If you wish to succeed, you should use persistence as your good friend, "
SIG = generate_sig(MESSAGE)

forged = False
psk_len = 0
for psk_len in range(0, 32):
    attacker_message, forged_sig = transfer_sig(MESSAGE, SIG, psk_len)
    print(f"攻击者提交了{psk_len}字节的PSK: {forged_sig}")
    forged = submit(attacker_message, forged_sig)
    if forged:
        print(f"\n攻击者伪造了签名. PSK的长度为{psk_len}字节")
        break