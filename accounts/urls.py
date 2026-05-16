# accounts/urls.py
from django.urls import path, include
from . import views


urlpatterns = [
    path('register/', views.register_page),
    path('login/', views.login_page),
    path('logout/', views.logout_view),
    path('profile/', views.profile_page),
    # path('change-password/', views.ChangePasswordAPIView.as_view(), name='api_change_password'),
    # path('status/', views.UserStatusAPIView.as_view(), name='api_status'),

]