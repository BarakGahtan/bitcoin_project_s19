import os, binascii, hashlib, base58, ecdsa

class Person:
    def __init__(self):
        self.private_key = 0
        self.public_key= 0
        self.address= 0
        # self.balance= 0


    def ripemd160(self,x):
        d = hashlib.new('ripemd160')
        d.update(x)
        return d

    def key_generator_func(self):
        for n in range(1):  # number of key pairs to generate`

            # generate private key , uncompressed WIF starts with "5"
            priv_key = os.urandom(32)
            fullkey = '80' + binascii.hexlify(priv_key).decode()
            sha256a = hashlib.sha256(binascii.unhexlify(fullkey)).hexdigest()
            sha256b = hashlib.sha256(binascii.unhexlify(sha256a)).hexdigest()
            WIF = base58.b58encode(binascii.unhexlify(fullkey + sha256b[:8]))
            # get public key , uncompressed address starts with "1"
            sk = ecdsa.SigningKey.from_string(priv_key, curve=ecdsa.SECP256k1)
            vk = sk.get_verifying_key()
            publ_key = '04' + binascii.hexlify(vk.to_string()).decode()
            hash160 = self.ripemd160(hashlib.sha256(binascii.unhexlify(publ_key)).digest()).digest()
            publ_addr_a = b"\x00" + hash160
            checksum = hashlib.sha256(hashlib.sha256(publ_addr_a).digest()).digest()[:4]
            publ_addr_b = base58.b58encode(publ_addr_a + checksum)
            i = n + 1

            print('Private Key    ', str(i) + ": " + WIF.decode())
            print("Bitcoin Address", str(i) + ": " + publ_addr_b.decode())
        self.private_key = WIF
        self.public_key = publ_key.decode()
        self.address = publ_addr_b
