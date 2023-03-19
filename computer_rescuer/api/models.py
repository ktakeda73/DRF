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
    email = models.CharField(max_length=64, db_index=True)
    default_password = models.CharField(max_length=100, db_index=True)
    default_salt = models.CharField(max_length=100)
    password = models.CharField(max_length=100, db_index=True)
    salt = models.CharField(max_length=100)
    dispatch = models.ForeignKey(to=Dispatch, on_delete=models.CASCADE)

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