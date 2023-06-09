import os
import jwt
import hashlib
import random, string
from computer_rescuer.settings import SECRET_KEY
from api.models import UserInfo
from rest_framework.authentication import get_authorization_header

def hash(password, salt):
    password = bytes(password, 'utf-8')
    salt = bytes(salt, 'utf-8')
    digest = hashlib.sha256(salt + password).hexdigest()
    
    for _ in range(100000):
        digest = hashlib.sha256(bytes(digest, 'utf-8')).hexdigest()
    return digest

def encode_sha256(password):
    password = bytes(password, 'utf-8')
    digest = hashlib.sha256(password).hexdigest()
    return digest

def editDatetime(datetime, editType):
    if editType == 'YYYYMMDDHHMM':
        ret = datetime.strftime('%Y%m%d%H%M')
    
    return ret

def userPKFromToken(request):
    jwt_ = request.META.get('HTTP_AUTHORIZATION').replace("RESCUER ","")
    token = decodeToken(jwt_)
    return token['userid']

def decodeToken(jwt_token):
    jwt_info = jwt.decode(jwt_token, SECRET_KEY)
    return jwt_info

def randomStr(n):
   randlst = [random.choice(string.ascii_letters + string.digits) for i in range(n)]
   return ''.join(randlst)