import secrets

# Generate a random SECRET_KEY
def generate_secret_key():
    return secrets.token_hex(24)

# Print the generated SECRET_KEY
print(generate_secret_key())