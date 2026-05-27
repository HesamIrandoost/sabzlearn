# courses/management/commands/generate_fake_data.py
from django.core.management.base import BaseCommand
from django.contrib.auth.hashers import make_password
from faker import Faker
from core.settings import base as settings
from django.core.files.base import ContentFile
from django.core.files import File
import os

from accounts.models import User, InstructorProfile
from courses.models import Course, Section, Video, Enrollment, VideoProgress


class Command(BaseCommand):
    help = 'Set profile images for all instructors'

    def __init__(self, *args, **kwargs):
        super(Command, self).__init__(*args, **kwargs)
        self.fake = Faker('fa_IR')

    def handle(self, *args, **options):
        # مسیر فایل عکس
        image_path = os.path.join(settings.MEDIA_ROOT, 'p.png')
        
        # بررسی وجود فایل
        if not os.path.exists(image_path):
            self.stdout.write(self.style.ERROR(f'❌ file {image_path} not exist'))
            self.stdout.write(self.style.WARNING('⚠️ لطفاً یک عکس با نام p.png در پوشه media قرار دهید'))
            return
        
        # باز کردن فایل عکس
        with open(image_path, 'rb') as f:
            image_file = ContentFile(f.read(), name='profile_image.png')
            
            # دریافت همه استادها
            instructors = InstructorProfile.objects.all()
            total = instructors.count()
            
            if total == 0:
                self.stdout.write(self.style.WARNING('⚠️ nothing instructor ins db!'))
                return
            
            self.stdout.write(self.style.SUCCESS(f'📸 adding profile {total} instructor...'))
            
            for index, instructor in enumerate(instructors, 1):
                # ذخیره عکس برای هر استاد
                instructor.profile_image.save(f'instructor_{instructor.id}.png', image_file, save=True)
                self.stdout.write(f'  ✅ {index}/{total} - {instructor.first_name} {instructor.last_name}')
        
        self.stdout.write(self.style.SUCCESS('✅ all profiles succesfulty'))