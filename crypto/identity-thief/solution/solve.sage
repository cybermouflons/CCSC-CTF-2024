from Cryptodome.Cipher import AES
from Cryptodome.Util.Padding import pad
from Cryptodome.Util.number import long_to_bytes
from hashlib import sha256

# From given output:
ciphertext = b'\xe9\x81\xd9mA\x98\xa8\x06\x0beO\xe2\x9c\xae\x91\x0cF\xf9gx\xb7\x81S\xf6\xb8\xb2\xcb\xd0\x93\x82\x01N\x99ea\x9aq\x17J%\xa5\xcbQ\xee\x08\xe2\xdfWQ2}\x1c7\xc3\x94\x8d\xa5\x84\x18\xbf\xcdr>]'

# Assigned values that don't really matter:
p = random_prime(2^101-1,True,2^100)
a = 124124
b = 789235692
F = GF(p)
E = EllipticCurve(F, [a, b])
G = E(0, 1, 0)

# now use it as shared secret
hash = sha256()
hash.update(str(G).encode())

key = hash.digest()[16:32]
iv = b'Identity_Thief!!'
cipher = AES.new(key, AES.MODE_CBC, iv)

flag = cipher.decrypt(ciphertext)
print(flag)
