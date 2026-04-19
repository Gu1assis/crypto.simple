import base64

# Modular Arithmetic Utils
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

def squareAndMultiply(base, exponent, m):
    """
    returns base**exponent (mod m)
    """
    binaryExponentString = bin(exponent)[2:]
    buffer = 1
    for i in range(len(binaryExponentString)):
        if binaryExponentString[i] == "1":
            buffer = ((buffer*buffer)*base) % m
        if binaryExponentString[i] == "0":
            buffer = (buffer*buffer) % m
    return buffer  


# Key Encoding utils
def der_encode_integer(n):
    """Pakcs and integer in the format ASN.1 DER (0x02)"""
    content = n.to_bytes((n.bit_length() + 7) // 8, 'big')
    
    # Rule from ASN.1: If most significant bit equais 1, 
    # add a null byte (0x00) at the front so that it becomes positive
    if content[0] & 0x80:
        content = b'\x00' + content
        
    return b'\x02' + encode_length(len(content)) + content

def encode_length(l):
    """encodes length from ASN.1"""
    if l <= 127:
        return bytes([l])
    else:
        # Se o comprimento for > 127, usamos a 'Long Form'
        content = l.to_bytes((l.bit_length() + 7) // 8, 'big')
        return bytes([0x80 | len(content)]) + content

def der_encode_sequence(payloads):
    """Packs a list of elements into a SEQUENCE (Tag 0x30)"""
    content = b"".join(payloads)
    return b'\x30' + encode_length(len(content)) + content

def decode_length(data, pos):
    """Reads (Length) from ASN.1 and returns (length, new_pos)"""
    first_byte = data[pos]
    if first_byte <= 127:
        return first_byte, pos + 1
    else:
        num_bytes = first_byte & 0x7F
        length_bytes = data[pos + 1 : pos + 1 + num_bytes]
        return int.from_bytes(length_bytes, 'big'), pos + 1 + num_bytes
    
# Load public and Private Keys

def load_public_key_pem(filename):
    with open(filename, "r") as f:
        lines = f.readlines()
    
    # Remove header/footer
    b64_data = "".join([line.strip() for line in lines if "-----" not in line])
    der_data = base64.b64decode(b64_data)
    
    # --- DER Parsing ---
    pos = 0
    
    # Verifies SEQUENCE (0x30)
    if der_data[pos] != 0x30:
        raise ValueError("Invalid ASN.1 sequence")
    pos += 1
    
    # Ignores SEQUENCE size
    _, pos = decode_length(der_data, pos)
    
    # Retrieves integer n (0x02)
    if der_data[pos] != 0x02:
        raise ValueError("Expected integer (n)")
    pos += 1
    n_len, pos = decode_length(der_data, pos)
    n_bytes = der_data[pos : pos + n_len]
    n = int.from_bytes(n_bytes, 'big')
    pos += n_len
    
    # Retrieves integer e (0x02)
    if der_data[pos] != 0x02:
        raise ValueError("Expected integer (e)")
    pos += 1
    e_len, pos = decode_length(der_data, pos)
    e_bytes = der_data[pos : pos + e_len]
    e = int.from_bytes(e_bytes, 'big')
    
    return n, e