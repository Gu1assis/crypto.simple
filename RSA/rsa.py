import base64

# Primes
p = 17
q = 19
e = 217 # 65537

def extended_gcd(a, b):
    """
    returns (gcd, x, y) such that a*x + b*y = gcd
    """
    if a == 0:
        return b, 0, 1
    
    gcd, x1, y1 = extended_gcd(b % a, a)
    
    # Atualiza x e y usando os resultados da recursão
    x = y1 - (b // a) * x1
    y = x1
    
    return gcd, x, y

def modular_inverse(a, m):
    """
    returns modular inverse of 'a' mod 'm'
    """
    gcd, x, y = extended_gcd(a, m)
    
    if gcd != 1:
        raise ValueError(f"Modular invese of {a} mod {m} does not exist (MDC != 1)")
    else:
        return x % m

def textToDecimalAscii(text: str):
    asciiCodes = [0] *len(text)
    for i in range(len(text)):
        asciiCodes[i] = ord(text[i])
    return asciiCodes

def squareAndMultiply(base, exponent, mod):

    binaryExponentString = bin(exponent)[2:]
    buffer = 1
    for i in range(len(binaryExponentString)):
        if binaryExponentString[i] == "1":
            buffer = ((buffer*buffer)*base) % mod
        if binaryExponentString[i] == "0":
            buffer = (buffer*buffer) % mod
    return buffer
    
# Retrieve Keys
n = p*q
eulerTotient = (p-1)*(q-1) #288
d = modular_inverse(e, eulerTotient)

def RSAalgorithmEncrypt(text: str):

    decimals = textToDecimalAscii(text)
    for i in range(len(decimals)):
        decimals[i] = squareAndMultiply(decimals[i], e, n)
    combined_bytes = b"".join(d.to_bytes(2, 'big') for d in decimals)
    base64String = base64.b64encode(combined_bytes).decode("utf-8")
    return base64String

def RSAalgorithmDecrypt(textBase64):

    print("Im trying")

myString = "fsaidf"
print(RSAalgorithmEncrypt(myString))
print(RSAalgorithmDecrypt(RSAalgorithmEncrypt(myString)))