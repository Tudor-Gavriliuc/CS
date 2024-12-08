# pip install cryptography
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.x509 import (
    NameOID, CertificateBuilder, BasicConstraints, Name, random_serial_number, NameAttribute, load_pem_x509_certificate
)
from datetime import datetime, timedelta, timezone
import os

# Paths to store the PKI files
BASE_DIR = "pki"
CA_DIR = os.path.join(BASE_DIR, "ca")
USERS_DIR = os.path.join(BASE_DIR, "users")
os.makedirs(CA_DIR, exist_ok=True)
os.makedirs(USERS_DIR, exist_ok=True)


# Step 1: Generate CA private key and self-signed certificate
def generate_ca():
    ca_key_path = os.path.join(CA_DIR, "rootCA.key")
    ca_cert_path = os.path.join(CA_DIR, "rootCA.pem")

    # Generate CA private key
    print("Generating CA private key...")
    ca_private_key = rsa.generate_private_key(
        public_exponent=65537, key_size=4096
    )
    with open(ca_key_path, "wb") as f:
        f.write(
            # Serializes the private key into a byte string
            ca_private_key.private_bytes(
                # Encoding the key in PEM format(Privacy-Enhanced Mail)
                encoding=serialization.Encoding.PEM,
                format=serialization.PrivateFormat.TraditionalOpenSSL,
                encryption_algorithm=serialization.NoEncryption()
            )
        )

    # Generate self-signed CA certificate
    print("Generating CA self-signed certificate...")

    # Same since it’s a self-signed certificate, meaning the CA is signing its own certificate
    subject = issuer = Name([
        NameAttribute(NameOID.COUNTRY_NAME, "US"),
        NameAttribute(NameOID.STATE_OR_PROVINCE_NAME, "California"),
        NameAttribute(NameOID.LOCALITY_NAME, "San Francisco"),
        NameAttribute(NameOID.ORGANIZATION_NAME, "My Organization"),
        NameAttribute(NameOID.COMMON_NAME, "My Root CA"),
    ])

    ca_cert = (
        CertificateBuilder()
        .subject_name(subject)
        .issuer_name(issuer)
        # Public key of the CA
        .public_key(ca_private_key.public_key())
        # Unique serial number for the certificate
        .serial_number(random_serial_number())
        # Validity period of the certificate
        .not_valid_before(datetime.now(timezone.utc))
        # Validity period of the certificate
        .not_valid_after(datetime.now(timezone.utc) + timedelta(days=3650))
        # Basic constraints extension to indicate that this is a CA certificate
        .add_extension(BasicConstraints(ca=True, path_length=None), critical=True)
        # Sign the certificate with the CA private key
        .sign(private_key=ca_private_key, algorithm=hashes.SHA256())
    )
    with open(ca_cert_path, "wb") as f:
        f.write(ca_cert.public_bytes(serialization.Encoding.PEM))

    print(f"CA setup complete: {ca_key_path}, {ca_cert_path}")


# Step 2: Generate user key and certificate signed by the CA
def generate_user_certificate(username):
    user_key_path = os.path.join(USERS_DIR, f"{username}.key")
    user_cert_path = os.path.join(USERS_DIR, f"{username}.crt")

    # Load CA private key and certificate
    with open(os.path.join(CA_DIR, "rootCA.key"), "rb") as f:
        ca_private_key = serialization.load_pem_private_key(f.read(), password=None)
    with open(os.path.join(CA_DIR, "rootCA.pem"), "rb") as f:
        ca_cert = load_pem_x509_certificate(f.read())

    # Generate user private key
    print(f"Generating private key for user: {username}...")
    user_private_key = rsa.generate_private_key(
        public_exponent=65537, key_size=2048
    )
    with open(user_key_path, "wb") as f:
        f.write(
            user_private_key.private_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PrivateFormat.TraditionalOpenSSL,
                encryption_algorithm=serialization.NoEncryption()
            )
        )

    # Generate user certificate signed by the CA
    print(f"Generating certificate for user: {username}...")
    subject = Name([
        NameAttribute(NameOID.COUNTRY_NAME, "US"),
        NameAttribute(NameOID.ORGANIZATION_NAME, username),
        NameAttribute(NameOID.COMMON_NAME, f"{username} Certificate"),
    ])
    user_cert = (
        CertificateBuilder()
        .subject_name(subject)
        .issuer_name(ca_cert.subject)
        .public_key(user_private_key.public_key())
        .serial_number(random_serial_number())
        .not_valid_before(datetime.now(timezone.utc))
        .not_valid_after(datetime.now(timezone.utc) + timedelta(days=365))
        .add_extension(BasicConstraints(ca=False, path_length=None), critical=True)
        .sign(private_key=ca_private_key, algorithm=hashes.SHA256())
    )
    with open(user_cert_path, "wb") as f:
        f.write(user_cert.public_bytes(serialization.Encoding.PEM))

    print(f"User certificate generated: {user_key_path}, {user_cert_path}")


# Step 3: Sign a file
def sign_file(username, file_path):
    signature_path = f"{file_path}.sig"
    with open(os.path.join(USERS_DIR, f"{username}.key"), "rb") as f:
        user_private_key = serialization.load_pem_private_key(f.read(), password=None)

    # Read the file to sign
    with open(file_path, "rb") as f:
        data = f.read()

    # Sign the file
    print(f"Signing file: {file_path}...")
    signature = user_private_key.sign(
        data,
        # (Probabilistic Signature Scheme) padding scheme for RSA
        padding.PSS(
            # Mask generation function (MGF) used in PSS, which is a key part of the padding scheme
            mgf=padding.MGF1(hashes.SHA256()),
            salt_length=padding.PSS.MAX_LENGTH,
        ),
        hashes.SHA256(),
    )
    with open(signature_path, "wb") as f:
        f.write(signature)

    print(f"File signed: {signature_path}")


# Step 4: Verify a file signature
def verify_signature(username, file_path, signature_path):
    # Load user certificate (not the public key directly)
    with open(os.path.join(USERS_DIR, f"{username}.crt"), "rb") as f:
        user_cert = load_pem_x509_certificate(f.read())

    # Extract the public key from the certificate
    user_public_key = user_cert.public_key()

    # Read the file and signature
    with open(file_path, "rb") as f:
        data = f.read()
    with open(signature_path, "rb") as f:
        signature = f.read()

    # Verify the signature
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


def print_menu():
    print("Choose an option:")
    print("1. Generate CA (Root Certificate Authority)")
    print("2. Generate User Certificate")
    print("3. Sign a File")
    print("4. Verify File Signature")
    print("5. Exit")


def main():
    while True:
        print()
        print_menu()
        choice = input("Enter your choice: ")

        if choice == "1":
            generate_ca()
        elif choice == "2":
            username = input("Enter the username for the certificate: ")
            generate_user_certificate(username)
        elif choice == "3":
            username = input("Enter the username for signing: ")
            file_path = input("Enter the file path to sign: ")
            sign_file(username, file_path)
        elif choice == "4":
            username = input("Enter the username for verification: ")
            file_path = input("Enter the file path to verify: ")
            signature_path = input("Enter the signature file path: ")
            verify_signature(username, file_path, signature_path)
        elif choice == "5":
            print("Exiting the program.")
            break
        else:
            print("Invalid choice. Please select a valid option.")


if __name__ == "__main__":
    main()