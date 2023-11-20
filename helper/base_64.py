import base64

username_password = input("username:password\n")
encoded_credentials = base64.b64encode(username_password.encode('utf-8')).decode('utf-8')

print(encoded_credentials)