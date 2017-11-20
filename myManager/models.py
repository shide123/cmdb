# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import AbstractUser
from datetime import datetime
# Create your models here.
class UserProfile(AbstractUser):
    nick_name = models.CharField(max_length=50, verbose_name=u'nicename', default='')
    profile = models.CharField('profile', default='', max_length=256)
    image = models.ImageField(upload_to='image/%Y/%m', default=u'image/default.png', verbose_name=u'head', max_length=100)
    class Meta:
        verbose_name = r'userInfo'
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.username

class EmailVerifyRecord(models.Model):
    code = models.CharField(max_length=20)
    email = models.EmailField(max_length=50)
    send_type = models.CharField(choices=(('register', u'register'), ('forget',u'forget')), max_length=10)
    send_time = models.DateTimeField(default=datetime.now)
    class Meta:
        verbose_name = u'verifyCode'
        verbose_name_plural = verbose_name

class UserMessage(models.Model):
    # 如果 为 0 代表全局消息，否则就是用户的 ID
    user = models.IntegerField(default=0, verbose_name='user')
    message = models.CharField(max_length=500, verbose_name='message')
    has_read = models.BooleanField(default=False, verbose_name='has_read')
    add_time = models.DateTimeField(default=datetime.now, verbose_name='add_time')

    class Meta:
        verbose_name = '用户消息'
        verbose_name_plural = verbose_name
