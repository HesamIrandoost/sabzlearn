# accounts/urls.py
from django.urls import path, include
from . import views


app_name = 'accounts'
urlpatterns = [
    # API endpoints
    path('register/', views.RegisterAPIView.as_view(), name='api_register'),
    path('login/', views.LoginAPIView.as_view(), name='api_login'),
    path('logout/', views.LogoutAPIView.as_view(), name='api_logout'),
    path('profile/', views.ProfileAPIView.as_view(), name='api_profile'),
    path('change-password/', views.ChangePasswordAPIView.as_view(), name='api_change_password'),
    path('status/', views.UserStatusAPIView.as_view(), name='api_status'),

]