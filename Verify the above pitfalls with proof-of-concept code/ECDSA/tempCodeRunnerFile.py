    messageA='wakuwaku'
    KeyA=Generate_key()
    kA=Generate_K()
    sigA=Sign(messageA,n,KeyA['private key'],G,kA)
    Alice={ 'message':messageA,
            'private key':KeyA['private key'],
            'K':kA,
            'signature':sigA}

    messageB='byebyebye'
    KeyB=Generate_key()
    kB=kA
    sigB=Sign(messageB,n,KeyB['private key'],G,kB)
    Bob={   'message':messageB,
            'private key':KeyB['private key'],
            'K':kB,
            'signature':sigB}

    print("//Alice can compute Bob 's private key//")
    dB_=Leaking_k(kA,Bob['signature'],Bob['message'])
    print("Bob 's private key:",Bob['private key'])
    print("computed key by Alice with the same k:",dB_)

    print("//Bob can compute Alice 's private key//")
    dA_=Leaking_k(kB,Alice['signature'],Alice['message'])
    print("Alice 's private key:",Alice['private key'])
    print("computed key by Bob with the same k:",dA_)