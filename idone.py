from flask import request,jsonify,make_response
from functools import wraps
import requests
import jwt
import traceback

BASE_URL = 'https://one.in-d.ai/'
VERIFY_URL = BASE_URL+'api/credits/verify/' 
LOG_URL = BASE_URL+'api/credits/log/'
API_TOKEN_URL = BASE_URL+'api/keys/token/' 

VERIFYING_KEY = '''
-----BEGIN PUBLIC KEY-----
MIICIjANBgkqhkiG9w0BAQEFAAOCAg8AMIICCgKCAgEA0ghIvDcuO7DIIXqyhYET
QP9/TeNHx+p4scaZ14F8WS4vV/wHMvp//WqKvZOZT7aQh8ihMfZXR2MZ63+yIJ7D
xIIG6ojJmwrQbk9DOIv3NCIBAG84+jKz6IFano5z2D1kx/DxDRFEdjyPwHMbVxEH
p41Z+hu2LcYNYHzmgsOsNmSYTwwGcaQdLl9+P488HLaXZoicq6cj41FKIynti0E6
H50+4ZstKzklwXj05aOxE9HPPVLGzSZxsOYcfKp4UR+f6iJIkPy8Jj7w3xd2/SVM
3RuxfIwuDREvX5EhmM2cKYBAf4Bp7OSUMecSM2nXsjDmfRhNHpP7IfqOk//BCsgC
l1Jh4hl5mPlOwaVSZ9EJSuQa8FzAmkTS8moK9BcGzc6r5NUYUBTbKRcNaxUnwhBC
ByvdswpRT4w8g6w0iclWNyCB1qMwZiqfUn94h5bC852oU25LTQn2V4ZJopuoVr62
FKC/xkq2Lhvfjq4Qzmr5nhEHPJRlt/9YPXXMeTjYKmc09o2h+dLshhWuSeKyOwcL
tj+Rip7lTTh7N090W2HBCss6CgwAER5NT+AOyzTajIDpbd6Zs3OHg/VJRTpn2vgf
0uo8htoGGulemwD/x4nXkVhYGdRxSqgYa4Vzip7+4afoDR+5bB9maXFhPuFYs19d
3Qkg79xUu6CHYj4B/tTsqpMCAwEAAQ==
-----END PUBLIC KEY-----
'''


def indone_auth(service_id):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            
            #pre function run
            auth_headers = request.headers.get('Authorization')
            
            if not auth_headers:
                apikey = request.headers.get('x-api-key')
                if not apikey:
                    return make_response(jsonify({
                        'message':'authorization headers or api key not given'
                    }),403)

                response = requests.get(
                    API_TOKEN_URL,headers={"x-api-key": apikey})

                status_code = response.status_code
                if status_code != 201:
                    return make_response(response.json(),status_code)

                token = response.json().get('access')

                if not token:
                    return make_response({
                        'message':'unable to auth the request'
                    },403)

                auth_headers = 'Bearer '+token
            
            token_split = auth_headers.split()
            if 'Bearer' != token_split[0]:
                return make_response(jsonify({'message':'bearer token not given'}),403)
        
            response = requests.post(
                VERIFY_URL,
                json={
                    "service_id":service_id
                },
                headers={
                    "Content-Type": "application/json",
                    "Authorization": auth_headers
                }
            )
            print(response.text)
            status_code = response.status_code
            if status_code != 200:
                return make_response(response.json(),status_code)

            user_data = jwt.decode(token_split[1], VERIFYING_KEY, algorithms=['RS256'])
            kwargs.update(user_data)

            #original function runs here
            data = func(*args, **kwargs)

            #post function run
            if data.status_code == 200:
                response = requests.post(
                    LOG_URL,
                    json={
                        "service_id":service_id
                    },
                    headers={
                        "Content-Type": "application/json",
                        "Authorization": auth_headers
                    }
                )
                if response.status_code != 200:
                    print("Alert: ",response.json())
                    pass
            return data
        return wrapper
    return decorator
