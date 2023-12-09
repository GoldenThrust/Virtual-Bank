import random

def generate_account_number():
    return "".join(str(random.randint(0, 9)) for _ in range(12))