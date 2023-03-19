from django.db import models
from django.utils import timezone

class Dispatch(models.Model):
    created_dt = models.DateTimeField(auto_now_add=True)
    updated_dt = models.DateTimeField(auto_now=True)
    corporation = models.CharField(max_length=100, unique=True, db_index=True)

class Workplace(models.Model):
    created_dt = models.DateTimeField(auto_now_add=True)
    updated_dt = models.DateTimeField(auto_now=True)
    workplace = models.CharField(max_length=100,db_index=True)
    dispatch = models.ForeignKey(to=Dispatch, on_delete=models.CASCADE)

class UserInfo(models.Model):
    created_dt = models.DateTimeField(auto_now_add=True) 
    updated_dt = models.DateTimeField(auto_now=True) 
    username = models.CharField(max_length=50, db_index=True)
    email = models.CharField(max_length=64, unique=True, db_index=True)
    default_password = models.CharField(max_length=100, db_index=True)
    default_salt = models.CharField(max_length=100)
    password = models.CharField(max_length=100, db_index=True)
    salt = models.CharField(max_length=100)
    dispatch = models.ForeignKey(to=Dispatch, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

class AttendanceInfo(models.Model):
    created_dt = models.DateTimeField(auto_now_add=True)
    updated_dt = models.DateTimeField(auto_now=True)
    username = models.ForeignKey(to=UserInfo, on_delete=models.CASCADE)
    attendance_date = models.CharField(max_length=8)
    attendance_time = models.CharField(max_length=4)
    workplace = models.ForeignKey(to=Workplace, on_delete=models.CASCADE)
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["username", "attendance_date"],
                name="attendance_unique"
            ),
        ]
        
class AbsenceReson(models.Model):
    created_dt = models.DateTimeField(auto_now_add=True)
    updated_dt = models.DateTimeField(auto_now=True)
    reson = models.CharField(max_length=50, unique=True, db_index=True)

class AbsenceDivison(models.Model):
    created_dt = models.DateTimeField(auto_now_add=True)
    updated_dt = models.DateTimeField(auto_now=True)
    division = models.CharField(max_length=50, unique=True, db_index=True)
    
class AbsenceInfo(models.Model):
    created_dt = models.DateTimeField(auto_now_add=True)
    updated_dt = models.DateTimeField(auto_now=True)
    username = models.ForeignKey(to=UserInfo, on_delete=models.CASCADE)
    absence_date = models.DateField(max_length=8)
    division = models.ForeignKey(to=AbsenceDivison, on_delete=models.CASCADE)
    reason = models.ForeignKey(to=AbsenceReson, on_delete=models.CASCADE)
    remarks = models.TextField(null=True)
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["username", "absence_date"],
                name="absence_unique"
            ),
        ]