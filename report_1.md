# Gavriliuc Tudor

# Caesar Cipher

The general formula:
```
c = (x + k) % 26
```
Where:
- `x` is the index of the character in the alphabet.
- `k` is the key.
- `% 26` ensures wrapping around the alphabet.

For decryption, the formula becomes:
```
m = (y - k) % 26
```
Where:
- `y` is the index of the cipher character in the alphabet.
- `k` is the key.

While this cipher is easy to implement, it is also easy to break due to its limited keyspace (only 25 keys).

### Example

For a message `"HELLO"` encrypted with a key `k = 3`, the encrypted text would be:
```
H -> K, E -> H, L -> O, L -> O, O -> R
```
Resulting in the encrypted message: `"KHOOR"`.

Task 1: Basic Caesar Cipher Implementation

### Task Description
The goal of this task is to implement the Caesar cipher for the English alphabet without using pre-existing encoding functions (e.g., ASCII or Unicode). The implementation should handle only uppercase letters (`A-Z`) and ignore spaces. The user can choose to encrypt or decrypt, and the program ensures the key is valid.

### Code Implementation

The key functions in the implementation are:

```python
def charToIndex(c):
    return ord(c) - ord('A')

def indexToChar(i):
    return chr(i + ord('A'))
```
These two functions handle converting characters to and from their respective indices in the alphabet, making it possible to perform the Caesar shift operations.

```python
def encrypt(text, key):
    encryptedText = ""
    for c in text:
        indexC = charToIndex(c)
        newIndex = (indexC + key) % 26
        encryptedText += indexToChar(newIndex)
    return encryptedText

def decrypt(text, key):
    decryptedText = ""
    for c in text:
        indexC = charToIndex(c)
        newIndex = (indexC - key) % 26
        decryptedText += indexToChar(newIndex)
    return decryptedText
```
- **`encrypt`**: Takes a text and shifts each letter by the key value.
- **`decrypt`**: Reverses the shift to retrieve the original text.

```python
def checkKey(key):
    if key < 0 or key > 25:
        print("Invalid key")
        return False
    return True
```
Ensures the key is valid by checking that it's between 1 and 25.

### Running the Task

The `mainTask1()` function allows users to choose between encrypting and decrypting a message, enter the key and text, and receive the encrypted or decrypted result.

```python
def mainTask1():
    print("Caesar algorithm for the English alphabet")
    while(True):
        print("Possible operations: \n1. Encrypt text \n2. Decrypt text")
        operation = input("Enter operation: ")
        if(operation == "1"):
            text = input("Enter text to encrypt: ").upper()
            text = removeSpaces(text)
            key = int(input("Enter key: "))
            if(not checkKey(key)):
                continue
            if(not checkText(text)):
                print("Invalid text")
                continue
            if checkKey(key) and checkText(text):
                print("Encrypted text: ", encrypt(text, key))
        elif(operation == "2"):
            text = input("Enter text to decrypt: ").upper()
            text = removeSpaces(text)
            key = int(input("Enter key: "))
            if(not checkKey(key)):
                print("Invalid key")
                continue
            if(not checkText(text)):
                print("Invalid text")
                continue
            if checkKey(key) and checkText(text):
                print("Decrypted text: ", decrypt(text, key))
```

---

Task 2: Caesar Cipher with Two Keys

### Task Description
To enhance the security of the basic Caesar cipher, a second key, `k2`, is introduced. This second key is a permutation of the alphabet generated from a keyword provided by the user. The second key makes the cipher more resistant to simple attacks like brute force.

### Code Implementation

#### Key Functions

**`create_permuted_alphabet`**: 
This function creates a new alphabet by using the keyword. It eliminates duplicates and appends the remaining letters from the normal alphabet.

```python
def create_permuted_alphabet(keyword):
    keyword = ''.join(sorted(set(keyword), key=keyword.index))  # Remove duplicates and preserve order
    alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    permuted_alphabet = keyword + ''.join([ch for ch in alphabet if ch not in keyword])
    return permuted_alphabet
```

**`encrypt`**:
Encrypts the text by shifting characters based on `k1` using the new permuted alphabet from `k2`.

```python
def encrypt(text, k1, k2):
    encryptedText = ""
    text = text.upper().replace(' ', '')  # Convert to upper case and remove spaces
    permuted_alphabet = create_permuted_alphabet(k2.upper())  # Generate permuted alphabet

    for c in text:
        if c in permuted_alphabet:
            indexC = charToIndex(c)
            newIndex = (indexC + k1) % 26
            encryptedText += permuted_alphabet[newIndex]
        else:
            encryptedText += c  # If character is not in the alphabet, just append it as is
    return encryptedText
```

**`decrypt`**:
Decrypts the text by reversing the shifts and using the permuted alphabet to retrieve the original message.

```python
def decrypt(text, k1, k2):
    decryptedText = ""
    text = text.upper().replace(' ', '')  # Convert to upper case and remove spaces
    permuted_alphabet = create_permuted_alphabet(k2.upper())  # Generate permuted alphabet

    for c in text:
        if c in permuted_alphabet:
            indexC = permuted_alphabet.index(c)
            newIndex = (indexC - k1) % 26
            decryptedText += indexToChar(newIndex)
        else:
            decryptedText += c  # If character is not in the alphabet, just append it as is
    return decryptedText
```

### Running the Task

In the `main()` function, users can choose to encrypt or decrypt a message using both `k1` (Caesar shift) and `k2` (keyword permutation).

```python
def main():
    while True:
        operation = input("Do you want to encrypt or decrypt? (enter 1 to 'encrypt' or 2 to 'decrypt'): ").lower()
        if operation not in ['1', '2']:
            print("Invalid operation. Please try again.")
            continue

        k1 = int(input("Enter the Caesar shift key (k1, between 1 and 25): "))
        if not 1 <= k1 <= 25:
            print("Invalid shift key. Please enter a number between 1 and 25.")
            continue

        k2 = input("Enter the second key (keyword with at least 7 characters): ").upper()
        if len(k2) < 7 or not k2.isalpha():
            print("Invalid second key. Please enter a valid keyword with at least 7 letters.")
            continue

        message = input("Enter the message: ").upper()
        message = removeSpaces(message)

        # Perform the encryption or decryption
        if operation == '1':
            print("Encrypted text: ", encrypt(message, k1, k2))
        else:
            print("Decrypted text: ", decrypt(message, k1, k2))

        cont = input("Do you want to perform another operation? (yes/no): ").lower()
        if cont != 'yes':
            break
```

---

## Conclusion

In Task 1, a simple Caesar cipher was used to encrypt and decrypt data using just one key. This was further developed in Task 2 with the addition of a second key, {k2}, which permutes the alphabet and greatly strengthens the cipher against brute-force attacks. The principles of modular arithmetic are used to both jobs, together with extra error management and input validation to guarantee proper operation.
