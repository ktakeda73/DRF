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
from api.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', Login.as_view()),
    path('url-login/', UrlLogin.as_view()),
    path('attendance/', Attendance.as_view()),
    path('user/add/', UserAdd.as_view()),
    path('user/password/', ChangePassword.as_view()),
    path('user/change/', UserChange.as_view()),
    path('absence/add/', AbsenceAdd.as_view()),
    path('absence/change/', AbsenceChange.as_view())
    
]
