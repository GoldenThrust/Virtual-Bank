from utils.constant import api_url
from django.contrib.auth import logout
import requests

class VerifyToken:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        cookies = request.COOKIES
        verification_response = requests.get(f'{api_url}users/verify', cookies=cookies)
        
        if verification_response.status_code != 200 and verification_response.json()['detail'] != 'success':
            print(f"Token verification failed: {verification_response.status_code}")
            logout(request)
        else:
            print("Token verified successfully")

        response = self.get_response(request)

        return response
