# courses/management/commands/generate_fake_data.py
from django.core.management.base import BaseCommand
from django.core.files.base import ContentFile
from django.conf import settings
from faker import Faker
import random
import os

from accounts.models import User, InstructorProfile
from courses.models import Course, Section, Video, Enrollment, VideoProgress


class Command(BaseCommand):
    help = 'insert persian dummy data'
 
    def __init__(self, *args, **kwargs):
        super(Command, self).__init__(*args, **kwargs)
        self.fake = Faker('fa_IR')
        self.eng_fake = Faker()  # برای عناوین انگلیسی
        self.used_phones = set()
        self.used_emails = set()

    def generate_phone_number(self):
        """تولید شماره تلفن با فرمت 09 و 9 رقم تصادفی"""
        while True:
            random_digits = ''.join([str(random.randint(0, 9)) for _ in range(9)])
            phone = f"09{random_digits}"
            if phone not in self.used_phones:
                self.used_phones.add(phone)
                return phone

    def generate_unique_email(self):
        """تولید ایمیل یونیک"""
        while True:
            email = self.fake.unique.email()
            if email not in self.used_emails:
                self.used_emails.add(email)
                return email

    def get_sample_video(self):
        """دریافت فایل نمونه ویدیو"""
        video_sample_path = os.path.join(settings.BASE_DIR, 'media', 'sample_video.webm')
        if os.path.exists(video_sample_path):
            with open(video_sample_path, 'rb') as f:
                return ContentFile(f.read(), name='video.webm')
        return None

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('شروع تولید دیتای فیک...'))
        
        sample_video = self.get_sample_video()
        if not sample_video:
            self.stdout.write(self.style.WARNING('فایل نمونه ویدیو یافت نشد!'))
        
        # لیست عناوین فارسی برای سکشن‌ها
        section_titles = [
            'مقدمه', 'آشنایی با مفاهیم پایه', 'نصب و راه‌اندازی', 
            'ساخت پروژه عملی', 'پیشرفته‌تر', 'بهینه‌سازی', 
            'اشکال‌زدایی', 'پروژه نهایی', 'جمع‌بندی', 'منابع اضافی'
        ]
        
        # ایجاد 20 مدرس
        for instructor_num in range(20):
            self.stdout.write(f'در حال ایجاد مدرس {instructor_num + 1}/20...')
            
            phone = self.generate_phone_number()
            email = self.generate_unique_email()
            password = "qwe123QWE@"
            
            user_teacher = User.objects.create_user(
                phone=phone,
                email=email,
                password=password,
                role='instructor',
                is_active=True,
                is_staff=True,
                is_instructor_approved=True
            )

            # تکمیل پروفایل مدرس
            teacher = InstructorProfile.objects.get(user=user_teacher)
            teacher.first_name = self.fake.first_name()
            teacher.last_name = self.fake.last_name()
            teacher.bio = self.fake.paragraph(nb_sentences=3)
            teacher.is_verified = True
            teacher.save()

            # ایجاد 4 دوره برای هر مدرس
            for course_num in range(4):
                course_title = self.eng_fake.sentence(nb_words=random.randint(2, 5))
                self.stdout.write(f'  دوره: {course_title}')
                
                course = Course.objects.create(
                    instructor=user_teacher,
                    title=course_title.rstrip('.'),
                    description=self.fake.paragraph(nb_sentences=5),
                    price=random.randint(100000, 1000000),
                    is_published=True
                )
                
                # تعداد سکشن‌های تصادفی (بین 3 تا 7)
                num_sections = random.randint(3, 7)
                selected_sections = random.sample(section_titles, num_sections)
                
                for section_index, section_title in enumerate(selected_sections, start=1):
                    section = Section.objects.create(
                        course=course,
                        title=f"{section_title}",
                        order=section_index
                    )
                    
                    # تعداد ویدیوهای تصادفی برای هر سکشن (بین 1 تا 4)
                    num_videos = random.randint(1, 4)
                    
                    for video_index in range(1, num_videos + 1):
                        video = Video.objects.create(
                            section=section,
                            title=self.eng_fake.sentence(nb_words=random.randint(4, 7)).rstrip('.'),
                            video_file=sample_video if sample_video else 'videos/default.webm',
                            duration=random.randint(180, 3600),  # 3 دقیقه تا 1 ساعت
                            order=video_index,
                            is_free=(video_index == 1 and section_index == 1)  # فقط ویدیوی اول رایگان
                        )
        
        self.stdout.write(self.style.SUCCESS(f'✅ تولید دیتا با موفقیت انجام شد!'))
        self.stdout.write(f'📊 آمار: 20 مدرس - 80 دوره - سکشن‌ها و ویدیوهای متعدد')