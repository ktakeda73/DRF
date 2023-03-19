import os
import json
import jwt
import hashlib
import base64
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
    print(digest)
    return digest

def editDatetime(datetime, editType):
    if editType == 'YYYYMMDDHHMM':
        ret = datetime.strftime('%Y%m%d%H%M')
    
    return ret

def decode_token(jwt_):
    tmp = jwt_.split('.')

    header = json.loads(base64.b64decode(tmp[0]).decode())
    payload = json.loads(base64.b64decode(tmp[1]).decode())

    return {'header': header}

def decodeToken(jwt_token):
    jwt_info = jwt.decode(jwt_token, SECRET_KEY)
    return jwt_info