from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.x509 import load_pem_x509_certificate
import os


def sign_file(username, file_path):
    signature_path = f"{file_path}.sig"
    user_key_path = os.path.join("pki", "users", f"{username}.key")

    with open(user_key_path, "rb") as f:
        user_private_key = serialization.load_pem_private_key(f.read(), password=None)

    with open(file_path, "rb") as f:
        data = f.read()

    print(f"Signing file: {file_path}...")
    signature = user_private_key.sign(
        data,
        padding.PSS(
            mgf=padding.MGF1(hashes.SHA256()),
            salt_length=padding.PSS.MAX_LENGTH,
        ),
        hashes.SHA256(),
    )
    with open(signature_path, "wb") as f:
        f.write(signature)

    print(f"File signed: {signature_path}")


def verify_signature(username, file_path, signature_path):
    user_cert_path = os.path.join("pki", "users", f"{username}.crt")

    with open(user_cert_path, "rb") as f:
        user_cert = load_pem_x509_certificate(f.read())

    user_public_key = user_cert.public_key()

    with open(file_path, "rb") as f:
        data = f.read()
    with open(signature_path, "rb") as f:
        signature = f.read()

    print(f"Verifying signature for: {file_path}...")
    try:
        user_public_key.verify(
            signature,
            data,
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH,
            ),
            hashes.SHA256(),
        )
        print("Signature verified successfully.")
    except Exception as e:
        print("Verification failed:", e)
