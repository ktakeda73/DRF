import json
import base64
from api.utils.auth import JWTAuthentication
from api.utils.tools import *
from django.db import transaction 
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from api.models import UserInfo, AbsenceReson

class UserInfoListView(APIView):
    '''
    {
        "limit" : int,
        "offset" : int,
        "department_id": int,
        "dispatch": int
    }
    '''
    authentication_classes = [JWTAuthentication, ]
    permission_classes = [IsAuthenticated, ]
    
    def get(self, request, *args, **kwargs):
        
        req = json.loads(request.body)
        condition = req.copy()
        del condition['limit']
        del condition['offset']
        
        results = UserInfo.objects.filter(**condition)[int(req['offset']) : int(req['limit']) + int(req['offset'])]
        results_list = list(results.values())
        for i in range(len(results_list)):
            del results_list[i]['created_dt']
            del results_list[i]['updated_dt']
            del results_list[i]['default_password']
            del results_list[i]['default_salt']
            del results_list[i]['password']
            del results_list[i]['salt']

        return Response({'status': 'OK', 'list': results_list})
    
class UserInfoView(APIView):
    authentication_classes = [JWTAuthentication, ]
    permission_classes = [IsAuthenticated, ]
    
    def get(self, request, *args, **kwargs):
        result = UserInfo.objects.filter(pk=json.loads(request.body)['id']).values()[0]
        del result['created_dt']
        del result['updated_dt']
        del result['default_password']
        del result['default_salt']
        del result['password']
        del result['salt']
        return Response({'status': 'OK', 'result': result})

class UserAddView(APIView):
    '''
    ユーザー追加
    {
    "username": str,
    "email" : str,
    "is_active" : bool,
    "is_superuser" : bool,
    "auth_name_id": int,
    "department_id": int,
    "dispatch_id" : int
    }
    '''
    authentication_classes = [JWTAuthentication, ]
    permission_classes = [IsAuthenticated, ]
    
    def put(self, request, *args, **kwargs):
        jwt_ = request.META.get('HTTP_AUTHORIZATION').replace("RESCUER ","")
        token = decodeToken(jwt_)
        userInfo = UserInfo.objects.get(pk=token['userid'])
        if not bool(userInfo.is_superuser):
            return Response({'detail':'ユーザー追加権限がありません'},status=400)
        lastUserid = UserInfo.objects.order_by('userid').reverse().first().userid
        try:
            userid_seq = int(lastUserid.replace('RESC','')) + 1
            userid = 'RESC' + '0' * (6 - len(str(userid_seq))) + str(userid_seq)
        except:
            userid = 'RESC000001'
            
        username = json.loads(request.body)['username']
        email = json.loads(request.body)['email']
        
        is_active = json.loads(request.body)['is_active']
        is_superuser = json.loads(request.body)['is_superuser']
        auth_name_id = json.loads(request.body)['auth_name_id']
        department_id = json.loads(request.body)['department_id']
        dispatch_id = json.loads(request.body)['dispatch_id']
        
        default_password = randomStr(10)
        salt = randomStr(100)
        password = encode_sha256(default_password)
        
        text = userid + '&' + email
        param = base64.b64encode(text.encode()).decode()
        urlParam = str(param[::-1])
        
        try:
            UserInfo.objects.create(userid=userid,
                                    user=username,
                                    email=email,
                                    default_password=password,
                                    default_salt=salt,
                                    password=password,
                                    salt=salt,
                                    is_active=is_active,
                                    is_superuser=is_superuser,
                                    auth_name_id=auth_name_id,
                                    department_id=department_id,
                                    dispatch_id=dispatch_id)
                                    
        except:
            return Response({'detail': 'ユーザーは既に存在します'},status=400)
        
        return Response({'status': 'OK',
                        'userid': userid,
                        'username': username,
                        'email': email,
                        'password': default_password, 
                        'is_active': is_active, 
                        'is_superuser': is_superuser, 
                        'auth_name_id': auth_name_id,
                        'dispatch_id': dispatch_id, 
                        'urlParam': urlParam},
                        status=200)

class UserChangeView(APIView):
    '''
    ユーザー変更
    id以外全項目任意
    {
    "id": int,
    "username" : str,
    "password": str,
    "is_active" : bool,
    "is_superuser" : bool,
    "auth_name_id" : int
    "dispatch_id" : int
    }
    '''
    authentication_classes = [JWTAuthentication, ]
    permission_classes = [IsAuthenticated, ]
    
    def put(self, request, *args, **kwargs):
        req = json.loads(request.body)
        userInfo = UserInfo.objects.get(pk=req['id'])
        if not bool(userInfo.is_superuser):
            return Response({'detail':'ユーザー変更権限がありません'})
        
        res ={}
        with transaction.atomic():
            for k, v in req.items():
                if k == 'email':
                    return Response({'detail': 'メールアドレスは変更できません'})
                elif k == 'username':
                    userInfo.user = v
                    res[k] = v
                elif k == 'password':
                    userInfo.password = encode_sha256(v)
                    userInfo.salt=randomStr(100)
                    res[k] = v
                elif k == 'is_active':
                    userInfo.is_active = v
                    res[k] = v
                elif k == 'is_superuser':
                    userInfo.is_superuser = v
                    res[k] = v
                elif k == 'auth_name_id':
                    userInfo.auth_name_id = v
                elif k == 'dispatch_id':
                    userInfo.dispatch_id = v
                    res[k] = v
            
            userInfo.save()
        
        return Response(res)
    
class ChangePassword(APIView):
    '''
    パスワード変更処理
    {
        "email": str,
        "password": str,
        "newest_password": str,
        "confirm_password": str
    }
    '''
    def put(self, request, *args, **kwargs):
        email = json.loads(request.body)['email']
        
        try:
            userInfo = UserInfo.objects.get(email=email)
        except:
            return Response({'detail': 'ユーザーが存在しません'})
        
        password=json.loads(request.body)['password']
        newest_password=json.loads(request.body)['newest_password']
        confirm_password=json.loads(request.body)['confirm_password']
        db_digest = hash(userInfo.password, userInfo.salt)
        digest = hash(encode_sha256(password), userInfo.salt)
        
        if digest != db_digest:
            return Response({'detail': 'パスワードが違います'})
        
        if newest_password != confirm_password:
            return Response({'detail': '新しいパスワードと新しいパスワード（確認）が違います'})
        
        if password == newest_password:
            return Response({'detail': '変更後のパスワードを入力してください'})
        
        userInfo.password = encode_sha256(newest_password)
        userInfo.salt=randomStr(100)
        userInfo.save()
        
        return Response({'status': 'OK', 'newest_password': newest_password})