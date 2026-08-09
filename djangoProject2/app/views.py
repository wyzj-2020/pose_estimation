import tempfile

from django.http import StreamingHttpResponse
from django.views.decorators import gzip
import time
from django.shortcuts import render, HttpResponse, redirect, HttpResponseRedirect
import cv2
from django.http import HttpRequest
import numpy as np
import threading
import os
import argparse
import torch
import sys
# from .forms import UploadFileForm

# dir_path = 'D:/pose_estimate/openpouseDemo/djangoProject2/openpose'
# os.environ['PATH'] = os.environ['PATH'] + ';' + dir_path + '/bin;'
import pyopenpose as op
import logging
import datetime

# 全局变量，用于存储摄像头视频流
frame = None
lock = threading.Lock()

# 开启一个线程来捕获摄像头视频流
# thread = threading.Thread(target=capture_video)
# thread.daemon = True
# thread.start()

# print(op)
# print("成功引入pyopenpose")

# parser = argparse.ArgumentParser()
#
params = dict()

params["model_folder"] = "D:/pose_estimate/openpouseDemo/djangoProject2/openpose/models/"
params["net_resolution"] = "368x256"

# 配置日志记录器
# logging.basicConfig(filename='openpose.log', level=logging.DEBUG)
#
# # 在初始化OpenPose引擎的地方添加日志记录
# logging.info('Initializing OpenPose engine...')
# # 执行OpenPose引擎初始化操作
# # 在初始化完成后添加日志记录，记录初始化结果
# logging.info('OpenPose engine initialized successfully.')
#
# # 在初始化OpenPose引擎之前打印相关参数的值
# print('Initializing OpenPose engine with parameters:', params)
# 初始化OpenPose引擎
opWrapper = op.WrapperPython()
opWrapper.configure(params)
opWrapper.start()
datum = op.Datum()

cap = cv2.VideoCapture(0)

# // 调用打开摄像头功能
# width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
# height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
c = 0



def video_feed(request):
    cap.release()
    def generate():
        cap=cv2.VideoCapture(0)
        # url = "rtsp://admin:123456@10.32.46.195:8554/live"
        while True:
            # 读取视频帧
            success, frame = cap.read()
            if not success or frame is None:
                continue
            font = cv2.FONT_HERSHEY_SIMPLEX
            datet = str(datetime.datetime.now())
            frame = cv2.resize(frame, (850, 600))
            frame = cv2.putText(frame, datet, (400, 50), font, 0.75, (255, 255, 255), 2, cv2.LINE_AA)
            # # print("开始")
            if len(frame) == 0:
                continue

            ret, jpeg = cv2.imencode('.jpg', frame)

            if not ret:
                continue

            # ret, jpeg = cv2.imencode('.jpg', frame)
            frame_bytes = jpeg.tobytes()

            # 将帧数据流发送给客户端
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')

    # 创建一个基于帧数据流的 HTTP 响应
    # cap.release()
    response = StreamingHttpResponse(generate(), content_type='multipart/x-mixed-replace; boundary=frame')
    return response

def video_process(request):
    cap.release()
    # print(request.method)
    # url = "rtsp://admin:123456@10.32.46.195:8554/live"
    # # 打开摄像头
    # output_dir = '/output/4/'
    # fps = cap.get(cv2.CAP_PROP_FPS)
    # size = (int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)), int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)))
    # framecount = cap.get(cv2.CAP_PROP_FRAME_COUNT)
    def generate():
        cap=cv2.VideoCapture(0)
        while True:
            # 读取视频帧
            success, frame = cap.read()
            if not success or frame is None:
                continue
            font = cv2.FONT_HERSHEY_SIMPLEX
            text = 'width:' + str(cap.get(3)) + 'height:' + str(cap.get(4))
            datet = str(datetime.datetime.now())
            # print(datet)
            img_resize = cv2.resize(frame, (850, 600))
            datum.cvInputData = img_resize
            opWrapper.emplaceAndPop(op.VectorDatum([datum]))  # openpose处理图像
            opframe = datum.cvOutputData
            opframe = cv2.putText(opframe, datet, (20, 50), font, 0.35, (255, 255, 255), 2, cv2.LINE_AA)
            if len(opframe) == 0:
                continue
            ret, jpeg = cv2.imencode('.jpg', opframe)
            if not ret:
                continue

            # ret, jpeg = cv2.imencode('.jpg', frame)
            frame_bytes = jpeg.tobytes()

            # 将帧数据流发送给客户端
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')

    # 创建一个基于帧数据流的 HTTP 响应
    response = StreamingHttpResponse(generate(), content_type='multipart/x-mixed-replace; boundary=frame')
    # cap.release()
    return response


# import torchlight
# import sys
# from torchlight import import_class
# from app.st_gcn.processor.demo_realtime import DemoRealtime
from .main import generate_real


def estimate(request):
    cap.release()
    response = generate_real()
    return response


def first_page(request):
    return render(request, 'first_page.html')


def page1(request):
    info = request.session.get('info')
    # print()
    if not info:
        return redirect('/login/')
    return render(request, 'page1.html', {'username': info[0]["username"]})


def pose(request):
    info = request.session.get('info')
    if not info:
        return redirect('/login/')
    return render(request, 'pose.html', {'username': info[0]["username"]})


def pose_estimate(request):
    info = request.session.get('info')
    if not info:
        return redirect('/login/')
    return render(request, 'pose_estimate.html', {'username': info[0]["username"]})


import base64
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from PIL import Image
from django.core.files import File
import tempfile
from django.core.files.base import ContentFile


@csrf_exempt
def save_img(request):
    if request.method == 'POST':
        info = request.session.get('info')
        # 解析 POST 数据中的图像数据
        image_data_url = request.POST.get('imageData')
        image_data = base64.b64decode(image_data_url.split(',')[1])
        if image_data:
            decoded_data = base64.b64decode(image_data)
            content_file = ContentFile(decoded_data)
            print(content_file)
            datet = str(datetime.datetime.now())
            filename = datet + '.jpg'
            em = info[0]["email"]
            models.ImgData.objects.create(email=em, image_filename=filename, image=content_file)
        # 在这里执行你的截图处理逻辑，例如保存图像到服务器
        # 返回 JSON 响应
        return JsonResponse({'success': True})
    else:
        return JsonResponse({'success': False, 'error': 'Invalid request method'})


def page3(request):
    cap.release()
    info = request.session.get('info')
    if not info:
        return redirect('/login/')
    return render(request, 'page3.html', {'username': info[0]["username"]})


# from .forms import UploadFileForm
from django.core.files.storage import FileSystemStorage


def page2(request):
    cap.release()
    info = request.session.get('info')
    if not info:
        return redirect('/login/')
    if request.method == 'POST':
        if 'file' in request.FILES:
            global saved_file_path
            file = request.FILES['file']  # 获取上传的文件对象
            if file.content_type == 'video/mp4':
                file_name = file.name
                if os.path.exists(file_name):
                    saved_file_path=file_name
                else:
                    fs=FileSystemStorage()
                    saved_file_path=fs.save(file_name,file)
                    saved_file_path=fs.url(saved_file_path)
                width, height = getSize(file)

                # print(width, height)
                # uploaded_file_url = fs.url(filename)  # 获取文件的URL，以便在网页上显示
                return render(request, 'page2.html', {'content2': '/demo_offline/', 'width': width, 'height': height,
                                                      'username': info[0]["username"]})
            else:
                return render(request, 'page2.html',
                              {'content': "please select a video or image file", 'username': info[0]["username"]})
        else:
            return render(request, 'page2.html', {'content': "No file selected", 'username': info[0]["username"]})

    #     if file.content_type == "image/jpeg":
    #     print(file)python
    #     print(file.name)
    #     fs = FileSystemStorage()  # 创建一个文件系统存储对象
    #     filename = fs.save(file.name, file)  # 将文件保存到指定的位置
    #     cap=cv2.VideoCapture(filename)
    #     uploaded_file_url = fs.url(filename)  # 获取文件的URL，以便在网页上显示
    #     return redirect('/page2')
    # else:
    #     return JsonResponse({'error':'No file '})
    # form = UploadFileForm()  # 如果请求不是POST或者没有文件，则创建一个新的表单对象
    return render(request, 'page2.html', {'username': info[0]["username"]})  # 渲染上传页面，并传递表单对象

import argparse
import sys

# torchlight
# import torchlight
from app.torchlight.torchlight import import_class

from .file_main import generate
def demo_offline(request):
    response,name=generate(saved_file_path)
    return response

def getSize(file):
    cap = cv2.VideoCapture(file.name)
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    cap.release()
    return width, height


# def generate_frame():
#     cap = cv2.VideoCapture(file.name)
#     while cap.isOpened():
#         # 读取视频帧
#         success, frame = cap.read()
#         if not success or frame is None:
#             continue
#         img_resize = cv2.resize(frame, (640, 520))
#         datum.cvInputData = img_resize
#         opWrapper.emplaceAndPop(op.VectorDatum([datum]))  # openpose处理图像
#         opframe = datum.cvOutputData
#         if len(opframe) == 0:
#             continue
#         ret, jpeg = cv2.imencode('.jpg', opframe)
#         if not ret:
#             continue
#
#         # ret, jpeg = cv2.imencode('.jpg', frame)
#         frame_bytes = jpeg.tobytes()
#         # 将帧数据流发送给客户端
#         yield (b'--frame\r\n'
#                b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')
#     cap.release()
#     # 创建一个基于帧数据流的 HTTP 响应


# def file_process(request):
#     return StreamingHttpResponse(generate_frame(), content_type='multipart/x-mixed-replace; boundary=frame')


from django import forms
from app.utils.encrypt import md5
from django.db import models
from . import models
from app.utils.code import check_code


# 用户认证

class UserInfo(forms.Form):
    username = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '用户名'}),
        max_length=120,
        label="用户名"
    )
    password = forms.CharField(
        max_length=120,
        label="密码",
        widget=forms.PasswordInput(render_value=True, attrs={'class': 'form-control', 'placeholder': '密码'}),
    )

    code = forms.CharField(
        label="验证码",
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '验证码'})
    )

    def clean_password(self):
        pwd = self.cleaned_data.get("password")
        return md5(pwd)


def login(request):
    if request.method == 'GET':
        form = UserInfo()
        return render(request, 'login.html', {'form': form})
    form = UserInfo(data=request.POST)
    if form.is_valid():
        user_code = form.cleaned_data.pop('code')
        code = request.session.get('image_code', "")
        if code.upper() != user_code.upper():
            form.add_error('code', "验证码错误")
            return render(request, 'login.html', {'form': form})
        # 数据库校验,获取用户对象
        # admin_object=models.Admin.objects.filter(password=form.cleaned_data['password'],email=form.cleaned_data['email']).first()
        admin_object = models.User.objects.filter(**form.cleaned_data).first()
        if not admin_object:
            # 显示错误信息
            form.add_error("password", "邮箱或密码错误")
            return render(request, 'login.html', {'form': form})
        # 获取用户
        # 网站随机生成字符串；
        request.session["info"] = {'id': admin_object.id, 'username': admin_object.username,
                                   'email': admin_object.email,'password':admin_object.password},
        # session保存7天
        request.session.set_expiry(60 * 60 * 24 * 7)
        return redirect('/page1/')
    return render(request, 'login.html', {'form': form})


from io import BytesIO


# 登录验证码
def image_code(request):
    img, code_string = check_code()
    # 写入session中，得到验证码
    request.session['image_code'] = code_string
    request.session.set_expiry(60)
    stream = BytesIO()

    img.save(stream, 'png')
    return HttpResponse(stream.getvalue())


def logout(request):
    request.session.clear()
    return redirect('/login/')


class logisterInfo(forms.Form):
    username = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '用户名'}),
        max_length=120,
        label="用户名"
    )
    email = forms.EmailField(
        max_length=120,
        label="邮箱",
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': '邮箱'}),

    )
    password = forms.CharField(
        max_length=120,
        label="密码",
        widget=forms.PasswordInput(render_value=True, attrs={'class': 'form-control', 'placeholder': '密码'}),
    )

    password_confirm = forms.CharField(
        max_length=120,
        label="确认密码",
        widget=forms.PasswordInput(render_value=True, attrs={'class': 'form-control', 'placeholder': '确认密码'}),

    )

    def clean_password(self):
        pwd = self.cleaned_data.get("password")
        return md5(pwd)

    def clean_password_confirm(self):
        pwd_confirm = self.cleaned_data.get("password_confirm")
        return md5(pwd_confirm)


def register(request):
    if request.method == 'GET':
        form = logisterInfo()
        return render(request, 'register.html', {'form': form})
    form = logisterInfo(data=request.POST)
    if form.is_valid():
        print("合格")
        name = form.cleaned_data.get("username")
        em = form.cleaned_data.get("email")
        pwd = form.cleaned_data.get("password")
        pwd_confirm = form.cleaned_data.get("password_confirm")
        if pwd != pwd_confirm:
            form.add_error("password_confirm", "密码不一致")
            return render(request, 'register.html', {'form': form})
        em_exist = models.User.objects.filter(email=em).exists()
        if em_exist:
            form.add_error("email", "邮箱已注册")
            return render(request, 'register.html', {'form': form})
        models.User.objects.create(username=name, email=em, password=pwd)
        # 数据库校验,获取用户对象
        # admin_object=models.Admin.objects.filter(password=form.cleaned_data['password'],email=form.cleaned_data['email']).first()
        return redirect('/login/')


def privacy(request):
    info = request.session.get('info')

    return render(request,'privacy.html',{'name':info[0]["username"], 'email':info[0]["email"]})