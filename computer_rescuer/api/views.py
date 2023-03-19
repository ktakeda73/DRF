import datetime
import base64
import json
import traceback
from rest_framework.views import APIView
from rest_framework.response import Response
from .utils.auth import NormalAuthentication, JWTAuthentication
from .utils.tools import editDatetime, decodeToken
from rest_framework.permissions import IsAuthenticated
from .models import AttendanceInfo

class Login(APIView):

    authentication_classes = [NormalAuthentication,]

    def post(self, request, *args, **kwargs):
        try:
            return Response({'token': request.user })
        except:
            return Response({'detail' : 'ERROR'})
        
class Attendance(APIView):
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
