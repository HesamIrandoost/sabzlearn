from rest_framework import generics, permissions
from django.shortcuts import get_object_or_404
from ..models import Section, Video
from ..api.serializers import VideoSerializer


class VideoListView(generics.ListCreateAPIView):
    """لیست و ایجاد ویدیوهای یک سکشن"""
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = VideoSerializer
    
    def get_queryset(self):
        section_id = self.kwargs.get('section_id')
        return Video.objects.filter(section_id=section_id)
    
    def perform_create(self, serializer):
        section_id = self.kwargs.get('section_id')
        section = get_object_or_404(Section, id=section_id, course__instructor=self.request.user)
        serializer.save(section=section)
