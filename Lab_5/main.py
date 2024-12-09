import os
from datetime import datetime, timedelta, timezone
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.x509 import (
    NameOID, CertificateBuilder, BasicConstraints, Name, random_serial_number, NameAttribute, load_pem_x509_certificate
)
from utils import sign_file, verify_signature

# Paths to store the PKI files
BASE_DIR = "pki"
CA_DIR = os.path.join(BASE_DIR, "ca")
USERS_DIR = os.path.join(BASE_DIR, "users")
os.makedirs(CA_DIR, exist_ok=True)
os.makedirs(USERS_DIR, exist_ok=True)


def generate_ca():
    ca_key_path = os.path.join(CA_DIR, "rootCA.key")
    ca_cert_path = os.path.join(CA_DIR, "rootCA.pem")

    print("Generating CA private key...")
    ca_private_key = rsa.generate_private_key(public_exponent=65537, key_size=4096)
    with open(ca_key_path, "wb") as f:
        f.write(
            ca_private_key.private_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PrivateFormat.TraditionalOpenSSL,
                encryption_algorithm=serialization.NoEncryption(),
            )
        )

    print("Generating CA self-signed certificate...")
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
        .public_key(ca_private_key.public_key())
        .serial_number(random_serial_number())
        .not_valid_before(datetime.now(timezone.utc))
        .not_valid_after(datetime.now(timezone.utc) + timedelta(days=3650))
        .add_extension(BasicConstraints(ca=True, path_length=None), critical=True)
        .sign(private_key=ca_private_key, algorithm=hashes.SHA256())
    )
    with open(ca_cert_path, "wb") as f:
        f.write(ca_cert.public_bytes(serialization.Encoding.PEM))

    print(f"CA setup complete: {ca_key_path}, {ca_cert_path}")


def generate_user_certificate(username):
    user_key_path = os.path.join(USERS_DIR, f"{username}.key")
    user_cert_path = os.path.join(USERS_DIR, f"{username}.crt")

    with open(os.path.join(CA_DIR, "rootCA.key"), "rb") as f:
        ca_private_key = serialization.load_pem_private_key(f.read(), password=None)
    with open(os.path.join(CA_DIR, "rootCA.pem"), "rb") as f:
        ca_cert = load_pem_x509_certificate(f.read())

    print(f"Generating private key for user: {username}...")
    user_private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
    with open(user_key_path, "wb") as f:
        f.write(
            user_private_key.private_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PrivateFormat.TraditionalOpenSSL,
                encryption_algorithm=serialization.NoEncryption(),
            )
        )

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
