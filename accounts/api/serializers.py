# accounts/serializers.py
from rest_framework import serializers
from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password
from accounts.models import User, StudentProfile, InstructorProfile

class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password_confirm = serializers.CharField(write_only=True, required=True)
    
    class Meta:
        model = User
        fields = ['phone', 'email', 'password', 'password_confirm']
        extra_kwargs = {
            'email': {'required': False, 'allow_blank': True},
            'phone': {'required': True},  # اضافه کنید

        }
    
    def validate(self, attrs):
        if attrs['password'] != attrs['password_confirm']:
            raise serializers.ValidationError({"password": "passwords dos'nt match"})
        return attrs
    
    def validate_phone(self, value):
        if User.objects.filter(phone=value).exists():
            raise serializers.ValidationError("this phone number already exists")
        return value
    
    def validate_email(self, value):
        """بررسی یکتایی ایمیل قبل از هر اقدامی"""
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("این ایمیل قبلاً ثبت نام کرده است")
        return value
    
    def create(self, validated_data):
        validated_data.pop('password_confirm')
        password = validated_data.pop('password')
        
        user = User.objects.create_user(
            phone=validated_data['phone'],
            email=validated_data['email'],
            password=password,
            role='student'  # همیشه دانشجو
        )
        return user


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'phone', 'email', 'role', 'is_instructor_approved', 'date_joined']
        read_only_fields = ['id', 'is_instructor_approved', 'date_joined']


class UserLoginSerializer(serializers.Serializer):
    phone = serializers.CharField(required=True)
    password = serializers.CharField(required=True, write_only=True)
    
    class Meta:
        model = User
        fields = ['phone', 'password']

    def validate(self, attrs):
        phone = attrs.get('phone')
        password = attrs.get('password')
        
        user = authenticate(request=self.context.get('request'), phone=phone, password=password)
        
        if not user:
            raise serializers.ValidationError("password or phone number is wrong")
        
        if not user.is_active:
            raise serializers.ValidationError("your account is disabled")
        
        attrs['user'] = user
        return attrs


class StudentProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    
    class Meta:
        model = StudentProfile
        fields = ['user', 'wallet_balance']

class InstructorProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    
    class Meta:
        model = InstructorProfile
        fields = ['user', 'profile_image', 'bio', 'is_verified', 'total_students', 'total_courses']

class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True, validators=[validate_password])
    confirm_new_password = serializers.CharField(required=True)
    
    def validate(self, attrs):
        if attrs['new_password'] != attrs['confirm_new_password']:
            raise serializers.ValidationError({"new_password": "password and confirm donsent match"})
        return attrs
    