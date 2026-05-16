# courses/management/commands/generate_teacher_fake_data.py
from django.core.management.base import BaseCommand
from django.core.files.base import ContentFile
from django.conf import settings
from faker import Faker
import random
import os

from accounts.models import User, InstructorProfile
from courses.models import Course, Section, Video


class Command(BaseCommand):
    help = 'تولید دیتای فیک فقط برای مدرس‌ها، دوره‌ها، سکشن‌ها و ویدیوها'
 
    def __init__(self, *args, **kwargs):
        super(Command, self).__init__(*args, **kwargs)
        self.fake = Faker('fa_IR')
        self.eng_fake = Faker()
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
        self.stdout.write(self.style.SUCCESS('🎯 شروع تولید دیتای فیک (فقط مدرس و دوره)'))
        self.stdout.write('='*50)
        
        sample_video = self.get_sample_video()
        if not sample_video:
            self.stdout.write(self.style.WARNING('⚠️ فایل نمونه ویدیو یافت نشد! ویدیوها بدون فایل ایجاد می‌شوند'))
        
        section_titles = [
            'مقدمه و آشنایی', 'مفاهیم پایه', 'نصب و راه‌اندازی', 
            'ساخت پروژه عملی', 'تکنیک‌های پیشرفته', 'بهینه‌سازی و عملکرد', 
            'اشکال‌زدایی و تست', 'پروژه نهایی', 'جمع‌بندی و گام‌های بعدی', 
            'منابع و لینک‌های مفید', 'تمرینات عملی', 'پرسش و پاسخ',
            'پروژه اول', 'پروژه دوم', 'تمرینات پایانی'
        ]
        
        instructors_list = []
        
        # ایجاد 20 مدرس
        self.stdout.write('\n📝 مرحله 1: ایجاد مدرس‌ها')
        self.stdout.write('-'*30)
        
        for instructor_num in range(20):
            self.stdout.write(f'در حال ایجاد مدرس {instructor_num + 1}/20...', ending=' ')
            
            phone = self.generate_phone_number()
            email = self.generate_unique_email()
            password = "qwe123QWE@"
            
            # ایجاد کاربر
            user_teacher = User.objects.create_user(
                phone=phone,
                email=email,
                password=password,
                role='instructor',
                is_active=True,
                is_staff=True,
                is_instructor_approved=True
            )
            
            # سیگنال به طور خودکار یه InstructorProfile خالی ساخته
            # حالا باید اون رو پیدا کنیم و آپدیت کنیم، نه اینکه دوباره بسازیم
            
            # پیدا کردن یا ساختن پروفایل (اگه سیگنال نساخته بود)
            instructor_profile, created = InstructorProfile.objects.get_or_create(
                user=user_teacher,
                defaults={
                    'first_name': self.fake.first_name(),
                    'last_name': self.fake.last_name(),
                    'bio': self.fake.paragraph(nb_sentences=3),
                    'is_verified': True,
                    'total_students': random.randint(100, 5000),
                    'total_courses': 0
                }
            )
            
            # اگه پروفایل قبلاً وجود داشت (توسط سیگنال ساخته شده)، اطلاعاتش رو آپدیت کن
            if not created:
                instructor_profile.first_name = self.fake.first_name()
                instructor_profile.last_name = self.fake.last_name()
                instructor_profile.bio = self.fake.paragraph(nb_sentences=3)
                instructor_profile.is_verified = True
                instructor_profile.total_students = random.randint(100, 5000)
                instructor_profile.save()
                self.stdout.write(self.style.SUCCESS(f'✅ آپدیت شد: {instructor_profile.first_name} {instructor_profile.last_name}'))
            else:
                self.stdout.write(self.style.SUCCESS(f'✅ ایجاد شد: {instructor_profile.first_name} {instructor_profile.last_name}'))
            
            instructors_list.append(instructor_profile)
        
        # ایجاد دوره‌ها برای هر مدرس
        self.stdout.write('\n📚 مرحله 2: ایجاد دوره‌ها، سکشن‌ها و ویدیوها')
        self.stdout.write('-'*30)
        
        total_courses = 0
        total_sections = 0
        total_videos = 0
        
        course_prefixes = [
            'آموزش جامع', 'دوره حرفه‌ای', 'مقدماتی تا پیشرفته', 
            'پروژه محور', 'صفر تا صد', 'کاربردی', 'تخصصی',
            'ورود به دنیای', 'مهارت‌های عملی', 'از پایه تا پیشرفته'
        ]
        
        course_topics = [
            'Python', 'JavaScript', 'React', 'Django', 'Flask',
            'Vue.js', 'Angular', 'Node.js', 'PHP', 'Laravel',
            'HTML/CSS', 'Bootstrap', 'Tailwind', 'Git', 'Docker',
            'PostgreSQL', 'MongoDB', 'Redis', 'REST API', 'GraphQL',
            'TypeScript', 'Next.js', 'Nuxt.js', 'FastAPI'
        ]
        
        for instructor in instructors_list:
            # هر مدرس بین 3 تا 6 دوره داشته باشه
            num_courses_for_instructor = random.randint(3, 6)
            
            for course_num in range(num_courses_for_instructor):
                course_title = f"{random.choice(course_prefixes)} {random.choice(course_topics)}"
                
                if random.random() > 0.7:
                    course_title = f"{random.choice(course_prefixes)} {random.choice(course_topics)} - {random.choice(['پروژه محور', 'عملی', 'متن باز', 'مدرن'])}"
                
                discount = random.choice([0, 10, 15, 20, 25, 30, 40, 50, 60, 70])
                is_published = random.choice([True, True, True, False])
                
                course = Course.objects.create(
                    instructor=instructor,
                    title=course_title,
                    description=f"{self.fake.paragraph(nb_sentences=5)}\n\n✨ سرفصل‌های دوره:\n{self.fake.paragraph(nb_sentences=8)}\n\n🎯 پیش‌نیازها:\n{self.fake.paragraph(nb_sentences=2)}",
                    price=random.randint(150000, 3500000),
                    discount_percent=discount,
                    is_published=is_published,
                    image=None
                )
                
                instructor.total_courses += 1
                instructor.save()
                total_courses += 1
                
                num_sections = random.randint(4, 12)
                selected_sections = random.sample(section_titles, min(num_sections, len(section_titles)))
                
                for section_index, section_title in enumerate(selected_sections, start=1):
                    section = Section.objects.create(
                        course=course,
                        title=section_title,
                        order=section_index
                    )
                    total_sections += 1
                    
                    num_videos = random.randint(2, 8)
                    
                    for video_index in range(1, num_videos + 1):
                        video_titles = [
                            f'قسمت {video_index}: {self.eng_fake.sentence(nb_words=random.randint(3, 6)).rstrip(".")}',
                            f'جلسه {video_index} - {self.eng_fake.sentence(nb_words=random.randint(4, 7)).rstrip(".")}',
                            self.eng_fake.sentence(nb_words=random.randint(4, 8)).rstrip('.')
                        ]
                        video_title = random.choice(video_titles)
                        
                        is_free_video = (section_index == 1 and video_index == 1) or (random.random() > 0.9)
                        
                        Video.objects.create(
                            section=section,
                            title=video_title,
                            video_file=sample_video if sample_video else 'videos/default.webm',
                            duration=random.randint(300, 7200),
                            order=video_index,
                            is_free=is_free_video
                        )
                        total_videos += 1
                
                published_status = "✅ منتشر شده" if is_published else "⏳ پیش‌نویس"
                self.stdout.write(f'  📚 {course_title} - {course.sections.count()} سکشن | {discount}% تخفیف | {published_status}')
        
        # آمار نهایی
        self.stdout.write(self.style.SUCCESS('\n' + '='*50))
        self.stdout.write(self.style.SUCCESS('✅ تولید دیتا با موفقیت انجام شد!'))
        self.stdout.write(self.style.SUCCESS('='*50))
        self.stdout.write(f'\n📊 آمار نهایی:')
        self.stdout.write(f'   👨‍🏫 مدرس: {len(instructors_list)} نفر')
        self.stdout.write(f'   📚 دوره: {total_courses} دوره')
        self.stdout.write(f'   📖 سکشن: {total_sections} سکشن')
        self.stdout.write(f'   🎬 ویدیو: {total_videos} ویدیو')
        self.stdout.write('='*50)
        
        if instructors_list:
            sample_instructor = instructors_list[0]
            sample_course = Course.objects.filter(is_published=True).first()
            self.stdout.write(f'\n🔍 نمونه اطلاعات:')
            self.stdout.write(f'   👨‍🏫 مدرس نمونه: {sample_instructor.first_name} {sample_instructor.last_name}')
            self.stdout.write(f'   📞 شماره تماس: {sample_instructor.user.phone}')
            if sample_course:
                final_price = sample_course.final_price
                self.stdout.write(f'   📚 دوره نمونه: {sample_course.title}')
                self.stdout.write(f'   💰 قیمت: {final_price:,} تومان')
                if sample_course.discount_percent > 0:
                    self.stdout.write(f'   🎁 تخفیف: {sample_course.discount_percent}%')
        
        self.stdout.write(self.style.SUCCESS('\n🎉 تمام!'))