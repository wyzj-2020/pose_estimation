from django.db import models
from django import forms
import base64

class User(models.Model):
    username = models.CharField(max_length=200)
    email = models.EmailField()
    password = models.CharField(max_length=200)

    def __str__(self):
        return self.username


class ImgData(models.Model):
    email = models.EmailField()
    image_filename = models.CharField(max_length=200,default=None)
    image = models.ImageField(upload_to='image/')

    def __str__(self):
        return self.email


# Create your models here.
# class VideoData(models.Model):
#     email = models.EmailField()
#     video_filename = models.CharField(max_length=200, default=None)
#     video = models.FileField(upload_to='video_process/')
#
#     def __str__(self):
#         return self.email