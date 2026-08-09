"""djangoProject2 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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

from app import views

urlpatterns = [
    path('', views.first_page, name="first_page"),
    path('register/', views.register, name="register"),
    path('logout/', views.logout, name='logout'),
    path('login/', views.login, name='login'),
    path('video_feed/', views.video_feed, name='video_feed'),
    path('video_process/', views.video_process, name='video_process'),
    path('admin/', admin.site.urls),
    path('page1/', views.page1, name='page1'),
    path('page2/', views.page2, name='page2'),
    # path('page3/', views.page3, name='page3'),
    # path('file_process/', views.file_process, name='file_process'),
    path('image/code/', views.image_code, name='image_code'),
    path('save/image/', views.save_img, name='save_img'),
    path('pose/', views.pose, name='pose'),
    path('pose_estimate/', views.pose_estimate, name='pose-ESTIMATE'),
    path('estimate/', views.estimate, name='estimate'),
    path('demo_offline/',views.demo_offline,name='demo_offline'),
    path('privacy/',views.privacy,name='privacy')
]
