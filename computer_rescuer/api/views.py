import datetime
import base64
import json
import traceback
from django.db import transaction 
from rest_framework.views import APIView
from rest_framework.response import Response
from .utils.auth import NormalAuthentication, UrlAuthentication, JWTAuthentication
from .utils.tools import *
from rest_framework.permissions import IsAuthenticated
from .models import *

class Login(APIView):

    authentication_classes = [NormalAuthentication,]

    def post(self, request, *args, **kwargs):
        try:
            return Response({'token': request.user })
        except:
            return Response({'detail' : 'ERROR'})
        
class UrlLogin(APIView):
    '''
    URLからログイン
    {
        "key": str
    }
    '''

    authentication_classes = [UrlAuthentication,]

    def post(self, request, *args, **kwargs):
        try:
            return Response({'token': request.user })
        except:
            return Response({'detail' : 'ERROR'})
        
class Attendance(APIView):
    '''
    出勤報告
    {
        "workspace": int
    }
    '''
    authentication_classes = [JWTAuthentication, ]
    permission_classes = [IsAuthenticated, ]

    def put(self, request, *args, **kwargs):
        now = datetime.datetime.now()
        attendance_date = editDatetime(now, 'YYYYMMDDHHMM')[:8]
        attendance_time = editDatetime(now, 'YYYYMMDDHHMM')[8:]
        workplace_id = json.loads(request.body)['workspace']
        jwt_ = request.META.get('HTTP_AUTHORIZATION').replace("RESCUER ","")
        token = decodeToken(jwt_)
        
        try:
            AttendanceInfo.objects.create(username_id=token['userid'], 
                                        attendance_date=attendance_date, 
                                        attendance_time=attendance_time, 
                                        workplace_id=workplace_id)
            pass
        except Exception as e:
            return Response({'detail': '出勤報告済', 'attendance_date': attendance_date[:4]+'/'+attendance_date[5:6]+'/'+attendance_date[7:8],'workplace_id': workplace_id})
        return Response({'status': 'OK', 
                        'username_id': token['userid'],
                        'attendance_date': attendance_date[:4]+'/'+attendance_date[5:6]+'/'+attendance_date[7:8],
                        'attendance_time': attendance_time[:2]+':'+attendance_time[:2],
                        'workplace_id': workplace_id})
    
class UserAdd(APIView):
    '''
    ユーザー追加
    {
    "username": str,
    "email" : str,
    "is_active" : bool,
    "is_superuser" : bool,
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
            return Response({'detail':'ユーザー追加権限がありません'})
        
        username = json.loads(request.body)['username']
        email = json.loads(request.body)['email']
        is_active = json.loads(request.body)['is_active']
        is_superuser = json.loads(request.body)['is_superuser']
        dispatch_id = json.loads(request.body)['dispatch_id']
        
        default_password = randomStr(10)
        salt = randomStr(100)
        password = encode_sha256(default_password)
        
        text = default_password + '&' + email
        param = base64.b64encode(text.encode()).decode()
        urlParam = str(param[::-1])
        try:
            UserInfo.objects.create(username=username,
                                    email=email,
                                    default_password=password,
                                    default_salt=salt,
                                    password=password,
                                    salt=salt,
                                    is_active=is_active,
                                    is_superuser=is_superuser,
                                    dispatch_id=dispatch_id)
        except:
            return Response({'detail': 'ユーザーは既に存在します'})
        return Response({'status': 'OK',
                        'username': username,
                        'email': email,
                        'password': default_password, 
                        'is_active': is_active, 
                        'is_superuser': is_superuser, 
                        'dispatch_id': dispatch_id, 
                        'urlParam': urlParam})

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

class UserChange(APIView):
    '''
    ユーザー変更
    id以外全項目任意
    {
    "id": int,
    "username" : str,
    "password": str,
    "is_active" : bool,
    "is_superuser" : bool,
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
                    userInfo.username = v
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
                elif k == 'dispatch_id':
                    userInfo.dispatch_id = v
                    res[k] = v
            
            userInfo.save()
        
        return Response(res)
    
class AbsenceAdd(APIView):
    '''
    欠勤情報追加
    {
        "absence_date": int,
        "division_id": int,
        "reason_id": int,
        "remarks": text
    }
    '''
    authentication_classes = [JWTAuthentication, ]
    permission_classes = [IsAuthenticated, ]
    
    def put(self, request, *args, **kwargs):
        req = json.loads(request.body)
        jwt_ = request.META.get('HTTP_AUTHORIZATION').replace("RESCUER ","")
        token = decodeToken(jwt_)
        absence_date = req['absence_date']
        division_id=req['division_id']
        reason_id=req['reason_id']
        username_id = token['userid']
        remarks = req['remarks']
        
        try:
            AbsenceInfo.objects.create(absence_date=absence_date,
                                       division_id=division_id,
                                       reason_id=reason_id,
                                        username_id=username_id,
                                        remarks=remarks)
        except:
            return Response({'detail': '欠勤情報は既に存在します'})
        return Response({'absence_date': absence_date,
                        'division_id': division_id,
                        'reason_id': reason_id,
                        'username_id': username_id,
                        'remarks': remarks
                         })
        

class AbsenceChange(APIView):
    authentication_classes = [JWTAuthentication, ]
    permission_classes = [IsAuthenticated, ]
    def put(self, request, *args, **kwargs):
        msg='欠勤情報が存在しません'
        req = json.loads(request.body)
        jwt_ = request.META.get('HTTP_AUTHORIZATION').replace("RESCUER ","")
        token = decodeToken(jwt_)
        id=req['id']
        try:
            absenceInfo = AbsenceInfo.objects.get(pk=id)
        except:
            return Response({'detail': msg})
        
        if token['userid'] != absenceInfo.username_id:
            return Response({'detail': msg})

        absenceInfo.absence_date = req['absence_date']
        absenceInfo.division_id = req['division_id']
        absenceInfo.reason_id = req['reason_id']
        absenceInfo.remarks = req['remarks']
        
        absenceInfo.save()