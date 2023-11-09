import random
import math

prime = set()
public_key = None
private_key = 42787  # Set a predefined private key value
n = 55637  # Set a predefined n value

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
    global public_key, n
    fi = (427 * 557)  # fi(n) based on predefined prime factors

    e = 65537  # Public exponent (commonly used value)

    public_key = e

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

if __name__ == '__main__':
    primefiller()
    setkeys()
    
    with open('test_file1', 'r') as file:
        content = file.read()
        encoded_content = encoder(content)

    with open('test_file1', 'w') as file:
        for num in encoded_content:
            file.write(f"{num} ")
