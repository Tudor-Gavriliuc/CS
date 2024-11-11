# Playfair Cipher Encryption and Decryption Tool

## Overview

This report describes the functionality of an interactive tool designed for encrypting and decrypting messages using the **Playfair Cipher** algorithm. The tool processes user input text, applies the Playfair Cipher rules with a user-defined key, and provides encrypted or decrypted text.

## Functionality

1. **Preparing Text for Encryption**:
   - The tool converts the input text to uppercase, removes non-alphabetic characters, and splits the text into pairs of letters.
   - It handles odd-length text by appending an "X" to the last letter if needed.

2. **Matrix Creation**:
   - A 6x5 cipher matrix is created based on a user-defined key.
   - The matrix is populated with unique letters from the key, followed by remaining letters of the alphabet (with "J" omitted). 
   - Romanian characters like Ș, Ț, Ă, Î, and Â are also supported.

3. **Letter Pair Encryption**:
   - Each letter pair is encrypted using the Playfair Cipher rules:
     - Letters in the **same row** are shifted **to the right**.
     - Letters in the **same column** are shifted **down**.
     - Letters in **different rows and columns** swap columns.

4. **Letter Pair Decryption**:
   - Each letter pair is decrypted by reversing the encryption rules:
     - Letters in the **same row** are shifted **to the left**.
     - Letters in the **same column** are shifted **up**.
     - Letters in **different rows and columns** swap columns.

5. **Output**:
   - After processing, the encrypted or decrypted text is displayed. Users can choose to encrypt or decrypt a message based on their provided key.

## Key Functions

- `prepare_text(text)`: Prepares text for encryption by converting to uppercase, removing non-alphabetic characters, and pairing letters.
- `create_cipher_matrix(key)`: Constructs a 6x5 matrix for encryption based on a unique set of letters from the key.
- `encrypt_pair(pair, matrix)`: Encrypts a pair of letters following the Playfair Cipher rules.
- `decrypt_pair(pair, matrix)`: Decrypts a pair of letters by reversing the encryption rules.
- `encrypt_message(plaintext, key)`: Encrypts an entire message using the matrix and Playfair rules.
- `decrypt_message(ciphertext, key)`: Decrypts an entire message using the matrix and reverse Playfair rules.

## Usage

- **Enter a Key**: The user inputs a key of at least 7 characters to create a cipher matrix.
- **Select an Operation**: Choose either encryption or decryption.
- **Enter Text**: Input the plaintext or ciphertext.
- **Apply Operation**: The tool encrypts or decrypts the text based on the selected operation.
- **View Output**: The resulting encrypted or decrypted text is displayed.

## Conclusion

This Playfair Cipher tool provides a simple and effective means of encrypting or decrypting messages. By creating a unique matrix from a user-defined key, it allows users to apply classical encryption techniques with real-time feedback.