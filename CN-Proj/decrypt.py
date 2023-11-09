import random
import math

prime = set()
public_key = None
private_key = None
n = None

def primefiller():
    seive = [True] * 250
    seive[0] = False
    seive[1] = False
    for i in range(2, 250):
        for j in range(i * 2, 250, i):
            seive[j] = False

    for i in range(len(seive)):
        if seive[i]:
            prime.add(i)

def pickrandomprime():
    global prime
    k = random.randint(0, len(prime) - 1)
    it = iter(prime)
    for _ in range(k):
        next(it)

    ret = next(it)
    prime.remove(ret)
    return ret

def setkeys():
    global public_key, private_key, n
    prime1 = pickrandomprime()  
    prime2 = pickrandomprime()

    n = prime1 * prime2
    fi = (prime1 - 1) * (prime2 - 1)

    e = 2
    while True:
        if math.gcd(e, fi) == 1:
            break
        e += 1
    public_key = e

    d = 2
    while True:
        if (d * e) % fi == 1:
            break
        d += 1

    private_key = d

def encrypt_decrypt_number(number, key, n):
    result = 1
    while key > 0:
        result = (result * number) % n
        key -= 1
    return result

def encoder(message):
    encoded = []
    for letter in message:
        encoded.append(encrypt_decrypt_number(ord(letter), public_key, n))
    return encoded

def decoder(encoded):
    decoded = []
    for num in encoded:
        decoded.append(encrypt_decrypt_number(num, private_key, n))
    return ''.join(chr(d) for d in decoded)

def encrypt_file(file_path):
    with open(file_path, 'r') as file:
        content = file.read()
        encoded_content = encoder(content)

    with open(file_path, 'w') as file:
        for num in encoded_content:
            file.write(f"{num} ")

def decrypt_file(file_path):
    with open(file_path, 'r') as file:
        encoded_content = list(map(int, file.read().split()))

    decoded_content = decoder(encoded_content)

    with open(file_path, 'w') as file:
        file.write(decoded_content)

    print("Contents of file after decryption:")
    print(decoded_content)

if __name__ == '__main__':
    primefiller()
    setkeys()
    
    # Encrypt the file
    encrypt_file('test_file1.txt')

    # Decrypt the file
    decrypt_file('test_file1.txt')
