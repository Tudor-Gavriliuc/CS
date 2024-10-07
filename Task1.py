def charToIndex(c):
    return ord(c) - ord('A')

def indexToChar(i):
    return chr(i + ord('A'))

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

def checkKey(key):
    if key < 0 or key > 25:
        print("Invalid key")
        return False
    return True

def checkText(text):
    return all(c.isalpha() for c in text)

def removeSpaces(text):
    return ''.join(text.split())

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


if __name__ == "__main__":
    mainTask1()