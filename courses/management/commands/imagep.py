# courses/management/commands/generate_fake_data.py
from django.core.management.base import BaseCommand
from django.contrib.auth.hashers import make_password
from faker import Faker
import random
from core import settings
from django.core.files.base import ContentFile
import os

from accounts.models import User, InstructorProfile
from courses.models import Course, Section, Video, Enrollment, VideoProgress


image_path = os.path.join(settings.MEDIA_ROOT, 'sample_image.png')
if os.path.exists(image_path):
    with open(image_path, 'rb') as f:
        video_file = ContentFile(f.read(), name='p.png')

class Command(BaseCommand):
    help = 'insert persian dummy data'
 
    def __init__(self, *args, **kwargs):
        super(Command, self).__init__(*args, **kwargs)
        self.fake = Faker('fa_IR')

    def handle(self, *args, **options):
        for i in range(2,22):
            instructor = InstructorProfile.objects.get(pk=i)
            instructor.profile_image = video_file
            instructor.save()




