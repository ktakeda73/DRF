import json
import base64
from api.utils.auth import JWTAuthentication, AuthUser
from api.utils.tools import *
from api.ERROR import *
from django.db import transaction 
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from api.models import UserInfo

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
        if not AuthUser.authKind(request, 'listview'):
            pk = userPKFromToken(request)
            results = UserInfo.objects.filter(pk=pk).values('id','userid','user','email','auth_name_id','department_id','dispatch_id')    
            return Response({'list': results})
        
        req = json.loads(request.body)
        condition = req.copy()
        del condition['limit']
        del condition['offset']
        
        results = UserInfo.objects.filter(**condition).values('id','userid','user','email','auth_name_id','department_id','dispatch_id')[int(req['offset']) : int(req['limit']) + int(req['offset'])]
        
        return Response({'list': results}, status=200)
    
class UserInfoView(APIView):
    '''
    ユーザー情報取得
    '''
    authentication_classes = [JWTAuthentication, ]
    permission_classes = [IsAuthenticated, ]
    
    def get(self, request, pk):
        try:
            if not(AuthUser.authKind(request, 'view')) and userPKFromToken(request) != pk:
                msg = getErrorMsg(AUTH_ERR, {'1':'ユーザー', '2': '閲覧'})
                return Response({'detail': msg},status=403)
            result = UserInfo.objects.filter(pk=pk).values('id','userid','user','email','auth_name_id','department_id','dispatch_id')[0]
            return Response({'result': result},status=200)
        except:
            return Response({'detail': SYS_ERR}, status=503)
        
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
    
    def _get_userid(self):
        try:
            lastUserid = UserInfo.objects.order_by('userid').reverse().first().userid
            userid_seq = int(lastUserid.replace('RESC','')) + 1
            userid = 'RESC' + '0' * (6 - len(str(userid_seq))) + str(userid_seq)
            return userid
        except:
            raise
        
    def _get_password(self):
        default_password = randomStr(10)
        salt = randomStr(100)
        password = encode_sha256(default_password)
        return default_password, salt, password

    def _loginUrl(self, userid, default_password):
        text = userid + '&' + default_password
        urlParam = str(base64.b64encode(text.encode()).decode())[::-1]
        return urlParam
    
    def post(self, request, *args, **kwargs):
        try:
            if not(AuthUser.authKind(request, 'add')):
                msg = getErrorMsg(AUTH_ERR, {'1':'ユーザー', '2': '追加'})
                return Response({'detail': msg},status=403)

            userid = self._get_userid()
        except:
            return Response({'detail': SYS_ERR},status=503)
        
        req = json.loads(request.body)
        default_password, salt, password = self._get_password()
        urlParam = self._loginUrl(userid, default_password)
        
        try:
            UserInfo.objects.create(userid=userid,user=req['username'],email=req['email'],
                                    default_password=password,default_salt=salt,password=password,
                                    salt=salt,is_active=req['is_active'],is_superuser=req['is_superuser'],auth_name_id=req['auth_name_id'],
                                    department_id=req['department_id'],dispatch_id=req['dispatch_id'])
                                    
        except:
            return Response({'detail': USER_EXIST_ERR},status=400)
        
        return Response({'userid': userid,'username': req['username'],'email': req['email'],
                        'password': default_password,'is_active': req['is_active'],'is_superuser': req['is_superuser'], 
                        'auth_name_id': req['department_id'],'dispatch_id': req['dispatch_id'], 'urlParam': urlParam},status=200)
        
class UserChangeView(APIView):
    '''
    ユーザー変更
    id以外全項目任意
    {
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
    def _shape(self, kwargs):
        password_str = None
        for k, v in list(kwargs.items()):
            if k =='id' or k == 'userid' or k =='pk' or k == 'default_password' or k == 'password':
                msg = {'detail': BODY_ERR}
                return Response(msg, 400)
            elif k == 'username':
                del kwargs['username']
                kwargs['user'] == v
            elif k == 'password_reset' and kwargs['password_reset']:
                password_str, salt, password = UserAddView._get_password(self)
                del kwargs['password_reset']
                kwargs['password'] = password
                kwargs['salt'] = salt
            
            if k == 'password_reset' and kwargs['password_reset'] == False:
                del kwargs['password_reset']
        
        return kwargs, password_str
    
    def _res(self,kwargs, password_str):
        for k, v in list(kwargs.items()):
            if k == 'password':
                del kwargs['salt']
                kwargs['password'] = password_str
        return kwargs
    
    def post(self, request, pk):
        kwargs = json.loads(request.body)

        if not(AuthUser.authKind(request, 'change')) and userPKFromToken(request) != pk:
            msg = getErrorMsg(AUTH_ERR, {'1':'ユーザー', '2': '変更'})
            return Response({'detail': msg},status=403)
        
        kwargs, password_str = self._shape(kwargs)
        
        try:
            UserInfo.objects.filter(pk=pk).update(**kwargs)
        except:
            msg = {'detail': FIELD_ERR}
            return Response(msg,status=403)
        
        kwargs = self._res(kwargs, password_str)
        return Response(kwargs)
    
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
    def _get_req(self, request):
        email = json.loads(request.body)['email']
        password=json.loads(request.body)['password']
        newest_password=json.loads(request.body)['newest_password']
        confirm_password=json.loads(request.body)['confirm_password']
        return email, password, newest_password, confirm_password
        
    def post(self, request, pk):
        email, password, newest_password, confirm_password = self._get_req(request)
        try:
            userInfo = UserInfo.objects.get(pk=pk)
        except:
            return Response({'detail': 'ユーザーが存在しません'})
        
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
        
        return Response({'newest_password': newest_password}, status=200)