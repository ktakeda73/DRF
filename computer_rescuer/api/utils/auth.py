import time
import json
import jwt
import base64
from computer_rescuer.settings import SECRET_KEY
from rest_framework.authentication import BaseAuthentication
from rest_framework import exceptions
from rest_framework.authentication import get_authorization_header
from .tools import hash, encode_sha256
from api.models import UserInfo

class NormalAuthentication(BaseAuthentication):
    
    def authenticate(self, request):
        param = json.loads(request.body)
        email = param['email']
        password = param['password']
        user_obj = UserInfo.objects.filter(email=email).first()
        msg = '認証失敗'
        if not user_obj:
            raise exceptions.AuthenticationFailed(msg)
        if not user_obj.is_active:
            raise exceptions.AuthenticationFailed(msg)
        db_digest = hash(user_obj.password, user_obj.salt)
        digest = hash(encode_sha256(password), user_obj.salt)
        if digest != db_digest:
            raise exceptions.AuthenticationFailed(msg)
        token = generate_jwt(user_obj)
        return (token, None)

    def authenticate_header(self, request):
        pass
    
class UrlAuthentication(BaseAuthentication):
    
    def authenticate(self, request):
        msg = '認証失敗'
        try:
            _url = json.loads(request.body)['key']
            reversed = str(_url[::-1])
            param = base64.b64decode(reversed).decode()
        except:
            raise exceptions.AuthenticationFailed(msg)
        email = param.split('&')[1]
        password = param.split('&')[0]
        user_obj = UserInfo.objects.filter(email=email).first()
        
        if not user_obj:
            raise exceptions.AuthenticationFailed(msg)
        if not user_obj.is_active:
            raise exceptions.AuthenticationFailed(msg)
        
        db_digest = hash(user_obj.default_password, user_obj.default_salt)
        digest = hash(encode_sha256(password), user_obj.default_salt)
        if digest != db_digest:
            raise exceptions.AuthenticationFailed(msg)
        token = generate_jwt(user_obj)
        return (token, None)

    def authenticate_header(self, request):
        pass

def generate_jwt(user):
    timestamp = int(time.time()) + 3600
    return jwt.encode(
        {"userid": user.pk, "email": user.email, "exp": timestamp},
        SECRET_KEY).decode("utf-8")

class JWTAuthentication(BaseAuthentication):
    keyword = 'rescuer'
    model = None
    msg = "AuthorizationError"

    def authenticate(self, request):
        auth = get_authorization_header(request).split()

        if not auth or auth[0].lower() != self.keyword.lower().encode():
            return None

        if len(auth) == 1:
            raise exceptions.AuthenticationFailed(msg)
        elif len(auth) > 2:
            raise exceptions.AuthenticationFailed(msg)

        try:
            jwt_token = auth[1]
            jwt_info = jwt.decode(jwt_token, SECRET_KEY)
            userid = jwt_info.get("userid")
            try:
                user = UserInfo.objects.get(pk=userid)
                user.is_authenticated = True
                if bool(user.is_active)==True:
                    return (user, jwt_token)
            except:
                raise exceptions.AuthenticationFailed(msg)
            
        except jwt.ExpiredSignatureError:
            msg = 'TokenTimeout'
            raise exceptions.AuthenticationFailed(msg)

    def authenticate_header(self, request):
        pass
