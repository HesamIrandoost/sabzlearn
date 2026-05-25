from django.shortcuts import render
from .serializers import ArticleListSerializer, ArticleDetailSerializer, ArticleCreateUpdateSerializer
from rest_framework import generics, permissions
from . models import Article, Tag
from core.permissons import IsInstructor
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi


# Create your views here.


class ArticleAPIView(generics.ListAPIView):
    """لیست همه مقالات برای همه"""

    permission_classes = [permissions.AllowAny]
    serializer_class = ArticleListSerializer
    def get_queryset(self):
        get_queryset = Article.objects.all()
        
        return get_queryset
    


class ArticleDetailAPIView(generics.RetrieveAPIView):
    """جزییهات هر دوره"""
    permission_classes = [permissions.AllowAny]
    serializer_class = ArticleDetailSerializer
    lookup_field = 'slug'

    def get_queryset(self):
        get_queryset = Article.objects.all()
        
        return get_queryset

class InstructorArticleListView(generics.ListCreateAPIView):
    """لیست مقاله های مدرس (و ایجاد مقاله جدید)"""
    permission_classes = [permissions.IsAuthenticated, IsInstructor]
    
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return ArticleCreateUpdateSerializer
        return ArticleListSerializer
    
    def get_queryset(self):
        return Article.objects.filter(author=self.request.user.instructor_profile)
    
    def perform_create(self, serializer):
        serializer.save(author=self.request.user.instructor_profile)

class InstructorArticleURDView(generics.RetrieveUpdateDestroyAPIView):
    """جزییات و اپدیت و حذف یک مقاله مخصوص مدرس"""
    permission_classes = [permissions.IsAuthenticated, IsInstructor]
    serializer_class = ArticleCreateUpdateSerializer
    lookup_field = 'slug'
    def get_queryset(self):
        return Article.objects.filter(author=self.request.user.instructor_profile)
