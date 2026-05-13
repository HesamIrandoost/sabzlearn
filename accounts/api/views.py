# accounts/views_api.py
from rest_framework import status, generics, views
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.authentication import BasicAuthentication, TokenAuthentication
from django.contrib.auth import login, logout
from rest_framework.authtoken.models import Token
from .serializers import (
    UserRegistrationSerializer, 
    UserLoginSerializer, 
    UserSerializer,
    StudentProfileSerializer,
    InstructorProfileSerializer,
    ChangePasswordSerializer)
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi



class RegisterAPIView(generics.CreateAPIView):
    """
    ثبت‌نام کاربر جدید (فقط دانشجو)
    """
    serializer_class = UserRegistrationSerializer
    permission_classes = [AllowAny]
    authentication_classes = []
    
    @swagger_auto_schema(
        operation_description="ثبت نام کاربر جدید در سیستم",
        operation_summary="ثبت نام",
        request_body=UserRegistrationSerializer,
        responses={
            201: openapi.Response('ثبت نام موفق', UserRegistrationSerializer),
            400: 'اطلاعات نامعتبر',
            409: 'ایمیل تکراری'
        },
        tags=['Authentication']
    )
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        
        # بعد از ثبت‌نام، لاگین خودکار انجام بشه
        login(request, user)
        
        # ساخت توکن
        token, created = Token.objects.get_or_create(user=user)
        
        return Response({
            # 'status': 'success',
            'message': 'ثبت نام موفقیت امیز بود',
            'user': user.role,
            'token': token.key
            # 'data': {
            #     'user': UserSerializer(user).data,
            #     'token': token.key
            # }
        }, status=status.HTTP_201_CREATED)


class LoginAPIView(generics.GenericAPIView):
    """
    ورود کاربر با شماره موبایل و رمز عبور
    """
    serializer_class = UserLoginSerializer
    permission_classes = [AllowAny]
    authentication_classes = []
    
    @swagger_auto_schema(
        operation_description="ورود به سیستم با شماره موبایل و رمز عبور",
        operation_summary="ورود",
        request_body=UserLoginSerializer,
        responses={
            200: 'ورود موفق',
            400: 'اطلاعات نامعتبر'
        },
        tags=['Authentication']
    )
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        
        user = serializer.validated_data['user']
        
        # لاگین کردن کاربر
        login(request, user)
        
        # ساخت یا دریافت توکن
        token, created = Token.objects.get_or_create(user=user)
        
        # دریافت اطلاعات پروفایل
        profile_data = None
        if user.role == 'student' and hasattr(user, 'student_profile'):
            profile_data = StudentProfileSerializer(user.student_profile).data
        elif user.role == 'instructor' and hasattr(user, 'instructor_profile'):
            profile_data = InstructorProfileSerializer(user.instructor_profile).data
        
        return Response({
            'message': 'Registration successful',
            'user': user.role,
            'token': token.key
            # 'status': 'success',
            # 'message': f'Welcome {user.phone}',
            # 'data': {
            #     'user': UserSerializer(user).data,
            #     'profile': profile_data,
            #     'token': token.key
            # }
        }, status=status.HTTP_200_OK)



class ProfileAPIView(generics.RetrieveUpdateAPIView):
    """
    دریافت و بروزرسانی پروفایل کاربر
    """
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    
    def get_serializer_class(self):
        if self.request.user.role == 'student':
            return StudentProfileSerializer
        elif self.request.user.role == 'instructor':
            return InstructorProfileSerializer
        return UserSerializer
    
    def get_object(self):
        if self.request.user.role == 'student':
            return self.request.user.student_profile
        elif self.request.user.role == 'instructor':
            return self.request.user.instructor_profile
        return self.request.user
    
    @swagger_auto_schema(
        operation_description="دریافت اطلاعات پروفایل کاربر",
        operation_summary="دریافت پروفایل",
        responses={
            200: 'دریافت موفق',
            401: 'احراز هویت نشده'
        },
        tags=['Profile']
    )
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response({
            'status': 'success',
            'data': serializer.data
        })
    
    @swagger_auto_schema(
        operation_description="بروزرسانی اطلاعات پروفایل کاربر",
        operation_summary="بروزرسانی پروفایل",
        request_body=StudentProfileSerializer,
        responses={
            200: 'بروزرسانی موفق',
            400: 'اطلاعات نامعتبر',
            401: 'احراز هویت نشده'
        },
        tags=['Profile']
    )
    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        
        return Response({
            'status': 'success',
            'message': 'Profile updated successfully',
            'data': serializer.data
        })


class LogoutAPIView(generics.GenericAPIView):
    """
    خروج از سیستم
    """
    permission_classes = [IsAuthenticated]
    authentication_classes = [BasicAuthentication, TokenAuthentication]
    
    @swagger_auto_schema(
        operation_description="خروج از سیستم و حذف توکن",
        operation_summary="خروج",
        responses={
            200: 'خروج موفق',
            401: 'احراز هویت نشده'
        },
        tags=['Authentication']
    )
    def post(self, request, *args, **kwargs):
        # حذف توکن
        try:
            request.user.auth_token.delete()
        except:
            pass
        
        # خروج از سیستم
        logout(request)
        
        return Response({
            'status': 'success',
            'message': 'Logout successful'
        }, status=status.HTTP_200_OK)


class ChangePasswordAPIView(generics.GenericAPIView):
    """
    تغییر رمز عبور
    """
    serializer_class = ChangePasswordSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [BasicAuthentication, TokenAuthentication]
    
    @swagger_auto_schema(
        operation_description="تغییر رمز عبور کاربر",
        operation_summary="تغییر رمز",
        request_body=ChangePasswordSerializer,
        responses={
            200: 'تغییر رمز موفق',
            400: 'اطلاعات نامعتبر',
            401: 'احراز هویت نشده'
        },
        tags=['Profile']
    )
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        user = request.user
        
        # بررسی رمز قدیم
        if not user.check_password(serializer.validated_data['old_password']):
            return Response({
                'status': 'error',
                'message': 'Current password is wrong'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # تنظیم رمز جدید
        user.set_password(serializer.validated_data['new_password'])
        user.save()
        
        # لاگین مجدد با رمز جدید
        login(request, user)
        
        return Response({
            'status': 'success',
            'message': 'Password changed successfully'
        }, status=status.HTTP_200_OK)


class UserStatusAPIView(generics.GenericAPIView):
    """
    بررسی وضعیت لاگین کاربر فعلی
    """
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    
    @swagger_auto_schema(
        operation_description="بررسی وضعیت احراز هویت کاربر",
        operation_summary="وضعیت کاربر",
        responses={
            200: 'کاربر احراز هویت شده',
            401: 'احراز هویت نشده'
        },
        tags=['Authentication']
    )
    def get(self, request, *args, **kwargs):
        user = request.user
        profile_data = None
        
        if user.role == 'student' and hasattr(user, 'student_profile'):
            profile_data = StudentProfileSerializer(user.student_profile).data
        elif user.role == 'instructor' and hasattr(user, 'instructor_profile'):
            profile_data = InstructorProfileSerializer(user.instructor_profile).data
        
        return Response({
            'status': 'success',
            'is_authenticated': True,
            'data': {
                'user': UserSerializer(user).data,
                'profile': profile_data
            }
        })