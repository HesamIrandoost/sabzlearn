# courses/management/commands/generate_fake_data.py
from django.core.management.base import BaseCommand
from django.contrib.auth.hashers import make_password
from faker import Faker
import random

from accounts.models import User
from courses.models import Course, Section, Video, Enrollment, VideoProgress


class Command(BaseCommand):
    help = 'insert persian dummy data'
 
    def __init__(self, *args, **kwargs):
        super(Command, self).__init__(*args, **kwargs)
        self.fake = Faker('fa_IR')
        self.used_phones = set()  # برای جلوگیری از تکرار شماره

    def generate_phone_number(self):
        """تولید شماره تلفن با فرمت 09 و 9 رقم تصادفی"""
        while True:
            # تولید 9 رقم تصادفی
            random_digits = ''.join([str(random.randint(0, 9)) for _ in range(9)])
            phone = f"09{random_digits}"
            
            # جلوگیری از تکرار در همین جلسه
            if phone not in self.used_phones:
                self.used_phones.add(phone)
                return phone

    def handle(self, *args, **options):
        
        for i in range(20):
            phone = self.generate_phone_number()
            User.objects.create_user(
                phone=phone,
                email=self.fake.unique.email(), 
                password="qwe123QWE@",
                role='student',
                is_active=True
            )
