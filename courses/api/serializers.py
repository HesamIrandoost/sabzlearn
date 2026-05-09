# courses/serializers.py
from rest_framework import serializers
from ..models import Course, Section, Video, Enrollment, VideoProgress
from accounts.models import User
from datetime import timezone

class UserSimpleSerializer(serializers.ModelSerializer):
    """سریالایزر ساده برای نمایش اطلاعات مدرس"""
    class Meta:
        model = User
        fields = ['phone', 'email']

class VideoSerializer(serializers.ModelSerializer):
    duration_minutes = serializers.ReadOnlyField()
    
    class Meta:
        model = Video
        fields = [
            'id', 'title', 'video_file', 'duration', 
            'duration_minutes', 'is_free', 'order', 'created_at'
        ]
        read_only_fields = ['id', 'created_at']

class SectionSerializer(serializers.ModelSerializer):
    videos = VideoSerializer(many=True, read_only=True)
    total_duration = serializers.ReadOnlyField()
    
    class Meta:
        model = Section
        fields = ['id', 'title', 'order', 'total_duration', 'videos']
        read_only_fields = ['id']

class CourseListSerializer(serializers.ModelSerializer):
    """سریالایزر برای لیست دوره‌ها (خلاصه)"""
    instructor_phone = serializers.ReadOnlyField(source='instructor.phone')
    final_price = serializers.ReadOnlyField()
    
    class Meta:
        model = Course
        fields = [
            'id', 'title', 'slug', 'instructor_phone', 
            'price', 'discount_percent', 'final_price', 
            'image', 'is_published', 'created_at'
        ]

class CourseDetailSerializer(serializers.ModelSerializer):
    """سریالایزر برای جزییات دوره (کامل)"""
    instructor = UserSimpleSerializer(read_only=True)
    sections = SectionSerializer(many=True, read_only=True)
    final_price = serializers.ReadOnlyField()
    total_duration = serializers.ReadOnlyField()
    is_enrolled = serializers.SerializerMethodField()
    progress_percent = serializers.SerializerMethodField()
    
    class Meta:
        model = Course
        fields = [
            'id', 'title', 'slug', 'description', 'instructor',
            'price', 'discount_percent', 'final_price', 'image',
            'sections', 'total_duration', 'is_published',
            'is_enrolled', 'progress_percent', 'created_at', 'updated_at'
        ]
    
    def get_is_enrolled(self, obj):
        """بررسی آیا کاربر فعلی در این دوره ثبت‌نام کرده"""
        user = self.context.get('request').user
        if user.is_authenticated and user.role == 'student':
            return Enrollment.objects.filter(student=user, course=obj).exists()
        return False
    
    def get_progress_percent(self, obj):
        """درصد پیشرفت کاربر در دوره"""
        user = self.context.get('request').user
        if user.is_authenticated and user.role == 'student':
            enrollment = Enrollment.objects.filter(student=user, course=obj).first()
            if enrollment:
                total_videos = Video.objects.filter(section__course=obj).count()
                if total_videos == 0:
                    return 0
                watched_videos = VideoProgress.objects.filter(
                    enrollment=enrollment, 
                    is_watched=True
                ).count()
                return int((watched_videos / total_videos) * 100)
        return 0

class CourseCreateUpdateSerializer(serializers.ModelSerializer):
    """سریالایزر برای ایجاد و بروزرسانی دوره (فقط مدرس)"""
    class Meta:
        model = Course
        fields = [
            'title', 'description', 'price', 'discount_percent', 
            'image', 'is_published'
        ]
    
    def validate_title(self, value):
        if Course.objects.filter(title=value).exists():
            raise serializers.ValidationError("دوره‌ای با این عنوان قبلاً ثبت شده")
        return value

class EnrollmentSerializer(serializers.ModelSerializer):
    course_title = serializers.ReadOnlyField(source='course.title')
    course_image = serializers.ReadOnlyField(source='course.image')
    progress_percent = serializers.SerializerMethodField()
    
    class Meta:
        model = Enrollment
        fields = [
            'id', 'course', 'course_title', 'course_image',
            'enrolled_at', 'is_completed', 'completed_at', 
            'progress_percent'
        ]
        read_only_fields = ['id', 'enrolled_at']
    
    def get_progress_percent(self, obj):
        """درصد پیشرفت در دوره"""
        total_videos = Video.objects.filter(section__course=obj.course).count()
        if total_videos == 0:
            return 0
        watched_videos = VideoProgress.objects.filter(
            enrollment=obj, 
            is_watched=True
        ).count()
        return int((watched_videos / total_videos) * 100)

class VideoProgressSerializer(serializers.ModelSerializer):
    video_title = serializers.ReadOnlyField(source='video.title')
    video_duration = serializers.ReadOnlyField(source='video.duration')
    
    class Meta:
        model = VideoProgress
        fields = [
            'id', 'video', 'video_title', 'video_duration',
            'is_watched', 'last_position', 'watched_at'
        ]
    
    def update(self, instance, validated_data):
        """بروزرسانی پیشرفت ویدیو"""
        if validated_data.get('is_watched', False) and not instance.is_watched:
            validated_data['watched_at'] = timezone.now()
        return super().update(instance, validated_data)