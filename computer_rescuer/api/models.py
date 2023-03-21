from django.db import models
from django.utils import timezone

class Dispatch(models.Model):
    created_dt = models.DateTimeField(auto_now_add=True)
    updated_dt = models.DateTimeField(auto_now=True)
    corporation = models.CharField(max_length=100, unique=True, db_index=True)
    class Meta:
        db_table = 'W01_Dispatch'
        
class Workplace(models.Model):
    created_dt = models.DateTimeField(auto_now_add=True)
    updated_dt = models.DateTimeField(auto_now=True)
    workplace = models.CharField(max_length=100,db_index=True)
    dispatch = models.ForeignKey(to=Dispatch, on_delete=models.CASCADE)
    class Meta:
        db_table = 'W02_Workplace'
        
class Department(models.Model):
    created_dt = models.DateTimeField(auto_now_add=True)
    updated_dt = models.DateTimeField(auto_now=True)
    department = models.CharField(max_length=100, unique=True, db_index=True)
    class Meta:
        db_table = 'W03_Department'
        
class AuthGroup(models.Model):
    created_dt = models.DateTimeField(auto_now_add=True)
    updated_dt = models.DateTimeField(auto_now=True)
    auth_name = models.CharField(max_length=50, unique=True)
    auth_group = models.CharField(max_length=17)
    user = models.CharField(max_length=17)
    attendance = models.CharField(max_length=17)
    leave = models.CharField(max_length=17)
    absence = models.CharField(max_length=17)
    holiday_work = models.CharField(max_length=17)
    expenses = models.CharField(max_length=17)
    class Meta:
        db_table = 'A01_Auth'
    
class UserInfo(models.Model):
    created_dt = models.DateTimeField(auto_now_add=True) 
    updated_dt = models.DateTimeField(auto_now=True) 
    userid = models.CharField(max_length=10,unique=True,db_index=True)
    user = models.CharField(max_length=50, db_index=True,db_column='username')
    email = models.CharField(max_length=64, unique=True, db_index=True)
    default_password = models.CharField(max_length=100, db_index=True)
    default_salt = models.CharField(max_length=100)
    password = models.CharField(max_length=100, db_index=True)
    salt = models.CharField(max_length=100)
    dispatch = models.ForeignKey(to=Dispatch, on_delete=models.PROTECT)
    is_active = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    auth_name = models.ForeignKey(to=AuthGroup, on_delete=models.PROTECT)
    department = models.ForeignKey(to=Department, on_delete=models.PROTECT)
    class Meta:
        db_table = 'F01_User'
        
class AttendanceInfo(models.Model):
    created_dt = models.DateTimeField(auto_now_add=True)
    updated_dt = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(to=UserInfo, on_delete=models.CASCADE)
    attendance_date = models.DateField(max_length=8)
    attendance_time = models.TimeField(max_length=4)
    workplace = models.ForeignKey(to=Workplace, on_delete=models.CASCADE)
    class Meta:
        db_table = 'F02_Attendance'
        constraints = [
            models.UniqueConstraint(
                fields=["user", "attendance_date"],
                name="attendance_unique"
            ),
        ]

class LeaveInfo(models.Model):
    created_dt = models.DateTimeField(auto_now_add=True)
    updated_dt = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(to=UserInfo, on_delete=models.CASCADE)
    leave_date = models.DateField(max_length=8)
    leave_time = models.TimeField(max_length=4)
    class Meta:
        db_table = 'F03_Leave'
        constraints = [
            models.UniqueConstraint(
                fields=["user", "leave_date"],
                name="leave_unique"
            ),
        ]
        
class AbsenceReson(models.Model):
    created_dt = models.DateTimeField(auto_now_add=True)
    updated_dt = models.DateTimeField(auto_now=True)
    reson = models.CharField(max_length=50, unique=True, db_index=True)
    class Meta:
        db_table = 'F04.01_Absence_Reason'
        
class AbsenceDivison(models.Model):
    created_dt = models.DateTimeField(auto_now_add=True)
    updated_dt = models.DateTimeField(auto_now=True)
    division = models.CharField(max_length=50, unique=True, db_index=True)
    class Meta:
        db_table = 'F04.02_Absence_Division'
        
class AbsenceInfo(models.Model):
    created_dt = models.DateTimeField(auto_now_add=True)
    updated_dt = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(to=UserInfo, on_delete=models.CASCADE)
    absence_date = models.DateField()
    division = models.ForeignKey(to=AbsenceDivison, on_delete=models.CASCADE)
    reason = models.ForeignKey(to=AbsenceReson, on_delete=models.CASCADE)
    remarks = models.TextField(null=True)
    class Meta:
        db_table = 'F04_Absence'
        constraints = [
            models.UniqueConstraint(
                fields=["user", "absence_date"],
                name="absence_unique"
            ),
        ]
        
class HolidayWorkInfo(models.Model):
    created_dt = models.DateTimeField(auto_now_add=True)
    updated_dt = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(to=UserInfo, on_delete=models.CASCADE)
    date = models.DateField()
    reson = models.TextField()    
    class Meta:
        db_table = 'F05_Holiday_Work'
        
class Expenses(models.Model):
    created_dt = models.DateTimeField(auto_now_add=True)
    updated_dt = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(to=UserInfo, on_delete=models.CASCADE)
    month = models.DateField()
    class Meta:
        db_table = 'F06_Expenses'
        
class ExpensesDetail(models.Model):
    created_dt = models.DateTimeField(auto_now_add=True)
    updated_dt = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(to=UserInfo, on_delete=models.CASCADE)
    date = models.DateField()
    division = models.IntegerField()
    is_from = models.CharField(max_length=40,null=True)
    is_to = models.CharField(max_length=40,null=True)
    round = models.BooleanField(null=True)
    amount = models.IntegerField()
    expenses = models.ForeignKey(to=Expenses,on_delete=models.CASCADE)
    class Meta:
        db_table = 'F06.01_Expenses_Detail'
