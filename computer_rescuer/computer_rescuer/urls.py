"""computer_rescuer URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from user.views import UserInfoListView, UserInfoView, UserAddView, UserChangeView, ChangePassword
from api.views import *


urlpatterns = [
    #認証
    path('login/', Login.as_view()),
    path('url-login/', UrlLogin.as_view()),
    
    #ユーザー
    path('user/list/', UserInfoListView.as_view()),
    path('user/info/', UserInfoView.as_view()),
    path('user/add/', UserAddView.as_view()),
    path('user/change/', UserChangeView.as_view()),
    path('user/password/', ChangePassword.as_view()),
    
    #出勤
    path('attendance/', Attendance.as_view()),
    
    #出勤報告
    path('absence/add/', AbsenceAdd.as_view()),
    path('absence/change/', AbsenceChange.as_view())
    
]
