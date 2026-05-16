# accounts/views.py (برای صفحات HTML)
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

# accounts/views.py
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json

def login_page(request):
    """نمایش صفحه ورود"""
    # اگه کاربر قبلاً لاگین کرده، بره به صفحه اصلی
    token = request.COOKIES.get('auth_token')
    if token:
        return redirect('/')
    return render(request, 'accounts/login.html')

def register_page(request):
    """نمایش صفحه ثبت نام"""
    token = request.COOKIES.get('auth_token')
    if token:
        return redirect('/')
    return render(request, 'accounts/register.html')

@login_required
def profile_page(request):
    """نمایش صفحه پروفایل"""
    return render(request, 'accounts/profile.html')

def logout_view(request):
    """خروج از حساب کاربری"""
    response = redirect('/login/')
    response.delete_cookie('auth_token')
    response.delete_cookie('user_phone')
    return response