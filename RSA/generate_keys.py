import secrets
import base64

import utils

# create big random odd number
def generate_large_odd_number(nbits):
    return secrets.randbits(nbits) | (1 << (nbits - 1)) | 1

# Miller rabin to find primes
def is_prime(n, k=40):
    """
    verifies if n is a prime using Miller-Rabin Test
    """
    predecessor = n-1
    baseTwoExponent = 0
    while predecessor % 2 != 1:
        predecessor = predecessor//2
        baseTwoExponent+= 1
    for _ in range(k):
        
        a = secrets.randbelow(n - 4) + 2
        x = utils.squareAndMultiply(a, predecessor, n)
        if x == 1 or x == n-1: continue
        
        for _ in range(baseTwoExponent-1):    
            x = utils.squareAndMultiply(x,2,n)
            if x == n-1: break
        else: return False
    return True

def get_large_prime(nbits):
    random_odd = generate_large_odd_number(nbits)

    while (not is_prime(random_odd)):
        random_odd = generate_large_odd_number(512)
    return random_odd

def save_public_key_pem(n,e, file_name="public_key.pem"):
    asn1_n = utils.der_encode_integer(n)
    asn1_e = utils.der_encode_integer(e)

    public_key_der = utils.der_encode_sequence([asn1_n, asn1_e])
    b64_content = base64.b64encode(public_key_der).decode('utf-8')
    formatted_b64 = "\n".join(b64_content[i:i+64] for i in range(0, len(b64_content), 64))
    with open(file_name, "w") as f:
        f.write("-----BEGIN RSA PUBLIC KEY-----\n")
        f.write(formatted_b64 + "\n")
        f.write("-----END RSA PUBLIC KEY-----\n")

# Define p,q, e and d

p = get_large_prime(512)
q = get_large_prime(512)

# Public keys:
e = 65537
n = p*q

save_public_key_pem(n, e)

eulerTotient = (p-1)*(q-1) #288
#validar antes de definir d
# Private key:
d = utils.modular_inverse(e, eulerTotient) # Private Key

print(n)

