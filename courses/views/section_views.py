from rest_framework import permissions
from rest_framework import generics
from ..api.serializers import SectionSerializer
from ..models import Section, Course
from django.shortcuts import get_object_or_404

class SectionListView(generics.ListCreateAPIView):
    """لیست و ایجاد سکشن‌های یک دوره"""
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = SectionSerializer
    
    def get_queryset(self):
        course_id = self.kwargs.get('course_id')
        return Section.objects.filter(course_id=course_id)
    
    def perform_create(self, serializer):
        course_id = self.kwargs.get('course_id')
        course = get_object_or_404(Course, id=course_id, instructor=self.request.user)
        serializer.save(course=course)

class SectionDetailView(generics.RetrieveUpdateDestroyAPIView):
    """مدیریت یک سکشن"""
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = SectionSerializer
    
    def get_queryset(self):
        return Section.objects.filter(course__instructor=self.request.user)
