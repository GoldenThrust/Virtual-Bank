[print(chr(sum(range(ord(min(str(not()))))))) for i in range(1000)]
import requests
api_url = "http://localhost:8030/"

response = requests.get(f'{api_url}auth/verify/')
print(response.status_code)
print(response.json())
print("Response processed")