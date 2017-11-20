# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.backends import ModelBackend
from django.db.models import Q
from django.views.generic.base import View
from django.contrib.auth.hashers import make_password
from django.http import HttpResponse, HttpResponsePermanentRedirect
from django.core.urlresolvers import reverse
from .models import UserProfile, EmailVerifyRecord, UserMessage
from .forms import LoginForm, RegisterForm, ForgetForm, ModifyPwdForm, UploadImageForm, UserInfoForm
from utils.email_send import send_register_email
from django.shortcuts import render_to_response


class RegisterView(View):
    def get(self, request):
        # get 请求的时候，把验证码组件一系列的 HTML render 到 register.html 里
        register_form = RegisterForm()
        return render(request, 'login.html', {'register_form': register_form})

    def post(self, request):
        register_form = RegisterForm(request.POST)
        if register_form.is_valid():
            email = request.POST.get('email', '')
            if UserProfile.objects.filter(email=email):
                return render(request, 'login.html', {'register_form': register_form, 'msg': '用户已经存在！'})
            password = request.POST.get('password', '')

            user_profile = UserProfile()
            user_profile.username = email
            user_profile.email = email
            user_profile.password = make_password(password)
            user_profile.is_active = False
            user_profile.save()

            #注册时发送一条消息
            user_message = UserMessage()
            user_message.user = user_profile.id
            user_message.message = '欢迎注册'
            user_message.save()
            send_register_email(email, 'register')
            return render(request, 'send_success.html')

        return render(request, 'login.html', {'register_form': register_form})

class LoginView(View):
    def get(self, request):
        return render(request, 'login.html')
    def post(self, request):
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            user_name = request.POST.get('username', '')
            password = request.POST.get('password', '')
            user = authenticate(username=user_name, password=password)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return HttpResponsePermanentRedirect(reversed('index'))
                return render(request, 'login.html', {'msg': '用户未激活！'})
            return render(request, 'login.html', {'msg': '用户名或者密码错误！'})
        return render(request, 'login.html', {'form_errors': login_form.errors})

class LogoutView(View):
    def get(self, request):
        logout(request)
        return HttpResponsePermanentRedirect(reverse('index'))

class RestView(View):
    def get(self, request, active_code):
        all_records = EmailVerifyRecord.objects.filter(code=active_code)
        if all_records:
            for records in all_records:
                email = records.email
                return render(request, 'login.html', {'email': email})
        return render(request, 'active_fail.html')

class IndexView(View):
    def get(self, request):
        return render(request, 'index.html')

class ModifyPwdView(View):
    def post(self, request):
        modify_form = ModifyPwdForm(request.POST)
        email = request.POST.get('email', '')
        if modify_form.is_valid():
            pwd1 = request.POST.get('password1', '')
            pwd2 = request.POST.get('password2', '')
            if pwd1 != pwd2:
                return render(request, 'login.html', {'email': email, 'msg':'密码不一致！'})
            user = UserProfile.objects.get(email=email)
            user = make_password(pwd2)
            user.save()
            return render(request,'login.html')
        return render(request, 'login.html', {'email': email, 'modify_form': modify_form})

class ForgetPwdView(View):
    def get(self, request):
        forget_form = ForgetForm()
        return render(request, 'login.html', {'forget_form':forget_form})

    def post(self,request):
        forget_form = ForgetForm(request.POST)
        if forget_form.is_valid():
            email = request.POST.get('email','')
            send_register_email(email,'forget')
            return render(request, 'send_success.html')
        return render(request, 'login.html', {'forget_form': forget_form})

def page_not_found(request):
    response = render_to_response('error_404.html', {})
    response.status_code = 404
    return response

def page_error(request):
    response = render_to_response('error_500.html', {})
    response.status_code = 500
    return response


