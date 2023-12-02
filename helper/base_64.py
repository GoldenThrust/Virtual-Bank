import base64

login_info = ["user_123:pass1234", "jane_doe:janedoe1", "sara_johnson:saraj456", "jdoe:jdoe1234", "emily_white:emily123", "jason_green:jasong123", "anna_brown:annab789", "max_miller:maxm1234", "lisa_wilson:lisaw123", "admin:admin"]

for login in login_info:
    encoded_credentials = base64.b64encode(login.encode('utf-8')).decode('utf-8')
    print(encoded_credentials)

