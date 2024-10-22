def removeSpaces(text):
    return ''.join(text.split())

def charToIndex(c):
    alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    return alphabet.index(c)

def indexToChar(index):
    alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    return alphabet[index]

def create_permuted_alphabet(keyword):
    # Create a permuted alphabet based on the keyword
    keyword = ''.join(sorted(set(keyword), key=keyword.index))  # Remove duplicates and preserve order
    alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    permuted_alphabet = keyword + ''.join([ch for ch in alphabet if ch not in keyword])
    return permuted_alphabet

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

if __name__ == "__main__":
    main()