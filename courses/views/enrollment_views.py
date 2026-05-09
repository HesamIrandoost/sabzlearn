from rest_framework import status, permissions, generics
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from ..models import Course, Enrollment, Video
from ..api.serializers import EnrollmentSerializer
from core.permissons import IsStudent

class EnrollCourseView(APIView):
    """ثبت‌نام در دوره (خرید دوره)"""
    permission_classes = [permissions.IsAuthenticated, IsStudent]
    
    def post(self, request, course_id):
        course = get_object_or_404(Course, id=course_id, is_published=True)
        
        # بررسی ثبت‌نام قبلی
        if Enrollment.objects.filter(student=request.user, course=course).exists():
            return Response({
                'status': 'error',
                'message': 'you have purchased in before'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # ایجاد ثبت‌نام
        enrollment = Enrollment.objects.create(student=request.user, course=course)
        
        return Response({
            'status': 'success',
            'message': 'purchased is successfuly',
            'data': EnrollmentSerializer(enrollment).data
        }, status=status.HTTP_201_CREATED)


class CourseContentAccessView(APIView):
    """دسترسی به محتوای دوره (بررسی ثبت‌نام یا رایگان بودن)"""
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request, course_slug, video_id=None):
        course = get_object_or_404(Course, slug=course_slug, is_published=True)
        video = get_object_or_404(Video, id=video_id)
        
        # اگر ویدیو رایگان باشه، دسترسی آزاد
        if video.is_free:
            return Response({
                'status': 'success',
                'video_url': video.video_file.url,
                'is_free': True
            })
        
        # بررسی ثبت‌نام
        if not Enrollment.objects.filter(student=request.user, course=course).exists():
            return Response({
                'status': 'error',
                'message': 'you have\'nt access this course, please purchased this course'
            }, status=status.HTTP_403_FORBIDDEN)
        
        return Response({
            'status': 'success',
            'video_url': video.video_file.url,
            'is_free': False
        })

class MyCoursesView(generics.ListAPIView):
    """دوره‌هایی که دانشجو خریداری کرده"""
    permission_classes = [permissions.IsAuthenticated, IsStudent]
    serializer_class = EnrollmentSerializer
    
    def get_queryset(self):
        return Enrollment.objects.filter(student=self.request.user)
