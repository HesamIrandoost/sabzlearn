from ..api.serializers import CourseListSerializer, CourseDetailSerializer, CourseCreateUpdateSerializer
from rest_framework import generics
from rest_framework import permissions
from ..models import Course 
from core.permissons import IsInstructor
from django.db.models import Q


class CourseListView(generics.ListAPIView):
    """لیست همه دوره‌های منتشر شده"""
    serializer_class = CourseListSerializer
    permission_classes = [permissions.AllowAny]
    
    def get_queryset(self):
        queryset = Course.objects.filter(is_published=True)
        
        # جستجو
        search = self.request.query_params.get('search', None)
        if search:
            queryset = queryset.filter(
                Q(title__icontains=search) | 
                Q(description__icontains=search)
            )
        
        # فیلتر بر اساس قیمت
        min_price = self.request.query_params.get('min_price', None)
        max_price = self.request.query_params.get('max_price', None)
        if min_price:
            queryset = queryset.filter(price__gte=min_price)
        if max_price:
            queryset = queryset.filter(price__lte=max_price)
        
        # مرتب‌سازی
        ordering = self.request.query_params.get('ordering', '-created_at')
        queryset = queryset.order_by(ordering)
        
        return queryset
    


class CourseDetailView(generics.RetrieveAPIView):
    """جزییات یک دوره"""
    serializer_class = CourseDetailSerializer
    permission_classes = [permissions.AllowAny]
    lookup_field = 'slug'
    
    def get_queryset(self):
        return Course.objects.filter(is_published=True)
    

class InstructorCourseListView(generics.ListCreateAPIView):
    """لیست دوره‌های مدرس (و ایجاد دوره جدید)"""
    permission_classes = [permissions.IsAuthenticated, IsInstructor]
    
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return CourseCreateUpdateSerializer
        return CourseListSerializer
    
    def get_queryset(self):
        return Course.objects.filter(instructor=self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(instructor=self.request.user)

class InstructorCourseDetailView(generics.RetrieveUpdateDestroyAPIView):
    """مدیریت یک دوره توسط مدرس"""
    permission_classes = [permissions.IsAuthenticated, IsInstructor]
    serializer_class = CourseCreateUpdateSerializer
    lookup_field = 'slug'
    
    def get_queryset(self):
        return Course.objects.filter(instructor=self.request.user)
