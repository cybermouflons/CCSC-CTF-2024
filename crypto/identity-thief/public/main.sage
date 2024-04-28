from Cryptodome.Cipher import AES
from Cryptodome.Util.Padding import pad
from Cryptodome.Util.number import long_to_bytes
from hashlib import sha256

from secret import FLAG, p, a, b, k1, k2, k3, priv_a, priv_b

F = GF(p)
E = EllipticCurve(F, [a, b])
G = E(p*k1, p*(k2 + 1/p), p*k3)

A = G * priv_a
B = G * priv_b

C = priv_a * B

assert C == priv_b * A

# now use it as shared secret
hash = sha256()
hash.update(str(C).encode())

key = hash.digest()[16:32]
iv = b'Identity_Thief!!'
cipher = AES.new(key, AES.MODE_CBC, iv)

encrypted = cipher.encrypt(pad(FLAG, 16))
print(encrypted)
