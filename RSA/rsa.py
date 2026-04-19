import base64
import utils

# Primes
p = 17
q = 19
e = 217 # 65537
# Mocked Keys
n = p*q
eulerTotient = (p-1)*(q-1) #288
d = utils.modular_inverse(e, eulerTotient) # Private Key
utils.modular_inverse(e, eulerTotient) # is e valid?

# Retrieve Keys
number, exp = utils.load_public_key_pem("public_key.pem")
print(exp)

def RSAalgorithmEncrypt(text: str):

    decimals = utils.textToDecimalAscii(text)
    for i in range(len(decimals)):
        decimals[i] = utils.squareAndMultiply(decimals[i], e, n)

    combined_bytes = b"".join(decimal.to_bytes(2, 'big') for decimal in decimals)
    return base64.b64encode(combined_bytes).decode("utf-8")

def RSAalgorithmDecrypt(textBase64: str):

    decryptedText = ""
    data_bytes = base64.b64decode(textBase64)
    for i in range(0, len(data_bytes), 2):
        chunk = data_bytes[i:i+2]
        decimal = int.from_bytes(chunk, 'big')
        decriptedDecimal = utils.squareAndMultiply(decimal, d, n)
        decryptedText += chr(decriptedDecimal)
    return decryptedText

myString = "fsaidf"
print(RSAalgorithmEncrypt(myString))
print(RSAalgorithmDecrypt(RSAalgorithmEncrypt(myString)))