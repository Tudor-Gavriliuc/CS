import random

# Tabelul PC-1 pentru permutarea cheii inițiale K+
PC1 = [
    57, 49, 41, 33, 25, 17, 9,
    1, 58, 50, 42, 34, 26, 18,
    10, 2, 59, 51, 43, 35, 27,
    19, 11, 3, 60, 52, 44, 36,
    63, 55, 47, 39, 31, 23, 15,
    7, 62, 54, 46, 38, 30, 22,
    14, 6, 61, 53, 45, 37, 29,
    21, 13, 5, 28, 20, 12, 4
]

# Numărul de shiftări pentru fiecare rundă
SHIFT_SCHEDULE = [1, 1, 2, 2, 2, 2, 2, 2, 1, 2, 2, 2, 2, 2, 2, 1]

def generate_random_key():
    """Generează o cheie aleatorie de 64 de biți."""
    return ''.join(random.choice('01') for _ in range(64))

def apply_permutation(table, key):
    """Aplică o permutare specifică pe un șir de biți."""
    return ''.join(key[i - 1] for i in table)

def left_shift(bits, shifts):
    """Realizează o deplasare circulară la stânga pe un șir de biți."""
    return bits[shifts:] + bits[:shifts]

def des_key_schedule(key_plus, i):
    """Calculează C_i și D_i pentru o rundă i dată."""
    # Pasul 1: Permutarea PC-1
    permuted_key = apply_permutation(PC1, key_plus)
    print(f"Cheia după permutarea PC-1: {permuted_key}")

    # Împărțirea în C și D
    c, d = permuted_key[:28], permuted_key[28:]
    print(f"Cheia C0: {c}")
    print(f"Cheia D0: {d}")

    # Aplicarea shiftărilor până la runda i
    for round_number in range(1, i + 1):
        shifts = SHIFT_SCHEDULE[round_number - 1]
        c = left_shift(c, shifts)
        d = left_shift(d, shifts)
        print(f"Runda {round_number}: C{round_number} = {c}, D{round_number} = {d}")

    return c, d

def main():
    print("Algoritmul DES: Calcularea C_i și D_i pentru un i dat.")
    option = input("Introduceți cheia manual (1) sau generați aleatoriu (2): ").strip()

    if option == '1':
        key_plus = input("Introduceți cheia de 64 biți (ex. 101010...): ").strip()
        if len(key_plus) != 64 or not all(bit in '01' for bit in key_plus):
            print("Cheia introdusă nu este validă. Asigurați-vă că are 64 de biți și conține doar 0 și 1.")
            return
    elif option == '2':
        key_plus = generate_random_key()
        print(f"Cheia generată aleatoriu este: {key_plus}")
    else:
        print("Opțiune invalidă.")
        return

    i = int(input("Introduceți numărul rundei i (1-16): ").strip())
    if not 1 <= i <= 16:
        print("Numărul rundei trebuie să fie între 1 și 16.")
        return

    # Calcularea cheilor C_i și D_i
    c_i, d_i = des_key_schedule(key_plus, i)
    print(f"Rezultatul final pentru runda {i}: C{i} = {c_i}, D{i} = {d_i}")

if __name__ == "__main__":
    main()
