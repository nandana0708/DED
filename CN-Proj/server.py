import os
from flask import Flask, request, render_template
from werkzeug.utils import secure_filename
import random
import math

app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

ALLOWED_EXTENSIONS = {'py', 'txt'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

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

prime = set()
public_key = None
private_key = None
n = None

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

def search_function_in_file(file_path, function_name):
    try:
        with open(file_path, 'r') as file:
            lines = file.readlines()
            for line_number, line in enumerate(lines, 1):
                if function_name in line:
                    return f"Function '{function_name}' found in {file_path} at line {line_number}:\n{line}"
    except FileNotFoundError:
        return f"File '{file_path}' not found."

def search_function_in_directory(root_directory, function_name):
    results = []
    for foldername, subfolders, filenames in os.walk(root_directory):
        for filename in filenames:
            if filename.endswith('.py'):
                file_path = os.path.join(foldername, filename)
                result = search_function_in_file(file_path, function_name)
                if result:
                    results.append(result)
                    #os.remove(file_path)
    return results

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            return "No file part"
        file = request.files['file']
        if file.filename == '':
            return "No selected file"
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)
            function_name_to_search = "encrypt_file(file_path)"
            results = search_function_in_directory(app.config['UPLOAD_FOLDER'], function_name_to_search)
            if results:
                os.remove(file_path)
                os.remove('/home/nandana/Documents/CN-Proj/test_file.py')
                return "File is malicious, removed from client device"
            else:
                return "File is safe"

    return render_template('upload_function.html')

@app.route('/decrypt', methods=['GET', 'POST'])
def upload_and_process_encryption():
    if request.method == 'POST':
        if 'file' not in request.files:
            return "No file part"
        file = request.files['file']
        if file.filename == '':
            return "No selected file"
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)
            if file_path.endswith('.txt'):
                primefiller()
                setkeys()
                encrypt_file(file_path)
                decrypt_file(file_path)
                #os.remove(file_path)  # Delete the text file
                return "Text file decrypted"
    return render_template('upload_encryption.html')

if __name__ == '__main__':
    if not os.path.exists(UPLOAD_FOLDER):
        os.mkdir(UPLOAD_FOLDER)
    app.run(debug=True)
