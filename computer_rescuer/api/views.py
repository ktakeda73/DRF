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