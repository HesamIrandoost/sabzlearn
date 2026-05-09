from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from accounts.models import User
# from accounts.models import User

class Course(models.Model):
    instructor = models.ForeignKey(
        User, 
        on_delete=models.CASCADE,
        related_name='courses',
        limit_choices_to={'role': 'instructor', 'is_instructor_approved': True}
    )
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True, blank=True)  # برای SEO
    description = models.TextField()
    price = models.PositiveIntegerField(default=0, help_text="قیمت به تومان")
    discount_percent = models.PositiveIntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(100)])
    image = models.ImageField(upload_to='courses/', null=True, blank=True)
    is_published = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['slug']),
            models.Index(fields=['-created_at']),
        ]
    
    @property
    def final_price(self):
        """محاسبه قیمت بعد از تخفیف"""
        if self.discount_percent > 0:
            return self.price - (self.price * self.discount_percent // 100)
        return self.price
    
    @property
    def total_duration(self):
        """مجموع زمان کل دوره"""
        total = 0
        for section in self.sections.all():
            total += section.total_duration
        return total
    
    def __str__(self):
        return self.title

class Section(models.Model):
    course = models.ForeignKey(
        Course, 
        on_delete=models.CASCADE,
        related_name='sections'
    )
    title = models.CharField(max_length=255)
    order = models.PositiveIntegerField(default=0)
    
    class Meta:
        ordering = ['order']
        unique_together = ['course', 'order']  # جلوگیری از order تکراری برای یک دوره
    
    def __str__(self):
        return f"{self.course.title} - {self.title}"
    
    @property
    def total_duration(self):
        """مجموع زمان ویدیوهای این بخش"""
        total = sum(video.duration for video in self.videos.all())
        return total

class Video(models.Model):
    section = models.ForeignKey(
        Section, 
        on_delete=models.CASCADE,
        related_name='videos'
    )
    title = models.CharField(max_length=255)
    video_file = models.FileField(upload_to='videos/%Y/%m/%d/')
    duration = models.PositiveIntegerField(help_text="مدت زمان به ثانیه")
    is_free = models.BooleanField(default=False)
    order = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['order']
        unique_together = ['section', 'order']
    
    def __str__(self):
        return self.title
    
    @property
    def duration_minutes(self):
        """نمایش زمان به دقیقه"""
        minutes = self.duration // 60
        seconds = self.duration % 60
        return f"{minutes}:{seconds:02d}"

# مدل برای ثبت خرید دوره‌ها
class Enrollment(models.Model):
    student = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='enrollments',
        limit_choices_to={'role': 'student'}
    )
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name='enrollments'
    )
    enrolled_at = models.DateTimeField(auto_now_add=True)
    is_completed = models.BooleanField(default=False)
    completed_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        unique_together = ['student', 'course']  # هر دانشجو فقط یکبار میتونه ثبت نام کنه
        ordering = ['-enrolled_at']
    
    def __str__(self):
        return f"{self.student.phone} - {self.course.title}"

# مدل برای پیشرفت دانشجو در هر ویدیو
class VideoProgress(models.Model):
    enrollment = models.ForeignKey(
        Enrollment,
        on_delete=models.CASCADE,
        related_name='video_progress'
    )
    video = models.ForeignKey(
        Video,
        on_delete=models.CASCADE,
        related_name='progress'
    )
    is_watched = models.BooleanField(default=False)
    last_position = models.PositiveIntegerField(default=0, help_text="آخرین ثانیه تماشا شده")
    watched_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        unique_together = ['enrollment', 'video']
    
    def __str__(self):
        return f"{self.enrollment.student.phone} - {self.video.title}"