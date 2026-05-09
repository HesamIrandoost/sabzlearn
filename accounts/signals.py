# accounts/signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from .models import StudentProfile, InstructorProfile

User = get_user_model()

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """ایجاد پروفایل مناسب بر اساس role کاربر"""
    if created:
        if instance.role == 'student':
            StudentProfile.objects.get_or_create(user=instance)
        elif instance.role == 'instructor':
            InstructorProfile.objects.get_or_create(user=instance)
        # برای admin هم می‌توانید اگر خواستید profile اضافه کنید