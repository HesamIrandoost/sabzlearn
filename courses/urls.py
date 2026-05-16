
# core/urls.py
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from .views.template_views import course_list_view, course_detail_view, video_player_view

urlpatterns = [
    path('', course_list_view, name='home'),
    path('course/<slug:course_slug>/', course_detail_view, name='course_detail'),
    path('video/<slug:course_slug>/<int:video_id>/', video_player_view, name='video_player'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)