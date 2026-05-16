# courses/management/commands/generate_fake_data.py
from django.core.management.base import BaseCommand
import random
import os
from django.conf import settings
from django.core.files.base import ContentFile
from courses.models import Course


class Command(BaseCommand):
    help = 'Set random cover images for all courses'
    
    def __init__(self, *args, **kwargs):
        super(Command, self).__init__(*args, **kwargs)
        # لیست آدرس تصاویر کاور (دقیقاً همون مسیرهایی که گفتی)
        self.cover_images = ['cover1.webp', 'cover2.webp', 'cover3.webp']
    
    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('🖼️ شروع فرآیند تنظیم کاور دوره‌ها...'))
        
        # گرفتن همه دوره‌ها
        courses = Course.objects.all()
        total_courses = courses.count()
        
        if total_courses == 0:
            self.stdout.write(self.style.WARNING('⚠️ هیچ دوره‌ای در دیتابیس وجود ندارد!'))
            return
        
        self.stdout.write(self.style.SUCCESS(f'📚 {total_courses} دوره پیدا شد.'))
        
        # بررسی کن ببینیم مدل چه فیلدی داره
        course_fields = [f.name for f in Course._meta.get_fields()]
        image_field = None
        
        # تشخیص فیلد تصویر
        if 'cover' in course_fields:
            image_field = 'cover'
        elif 'image' in course_fields:
            image_field = 'image'
        elif 'thumbnail' in course_fields:
            image_field = 'thumbnail'
        elif 'course_image' in course_fields:
            image_field = 'course_image'
        else:
            self.stdout.write(self.style.ERROR(f'❌ فیلد تصویر در مدل Course پیدا نشد!'))
            self.stdout.write(self.style.WARNING(f'فیلدهای موجود: {", ".join(course_fields)}'))
            return
        
        self.stdout.write(self.style.SUCCESS(f'✅ از فیلد "{image_field}" استفاده میشود.'))
        
        successful = 0
        failed = 0
        
        for index, course in enumerate(courses, 1):
            try:
                # انتخاب رندوم یک تصویر از لیست
                selected_image = random.choice(self.cover_images)
                image_path = os.path.join(settings.MEDIA_ROOT, selected_image)
                
                # بررسی وجود فایل
                if not os.path.exists(image_path):
                    self.stdout.write(self.style.WARNING(f'⚠️ فایل {selected_image} در مسیر {image_path} وجود ندارد'))
                    failed += 1
                    continue
                
                # باز کردن و ذخیره فایل
                with open(image_path, 'rb') as f:
                    image_file = ContentFile(f.read(), name=f'course_{course.id}_{selected_image}')
                    
                    # ذخیره در فیلد تشخیص داده شده
                    getattr(course, image_field).save(f'course_{course.id}_{selected_image}', image_file, save=True)
                    course.save()
                    successful += 1
                    
                    # نمایش پیشرفت
                    self.stdout.write(f'✅ {index}/{total_courses} - {course.title} -> {selected_image}')
                
            except Exception as e:
                failed += 1
                self.stdout.write(self.style.ERROR(f'❌ خطا برای دوره {course.title}: {str(e)}'))
        
        # گزارش نهایی
        self.stdout.write(self.style.SUCCESS('\n' + '='*50))
        self.stdout.write(self.style.SUCCESS(f'✅ عملیات با موفقیت به پایان رسید!'))
        self.stdout.write(self.style.SUCCESS(f'📸 موفق: {successful} دوره'))
        if failed > 0:
            self.stdout.write(self.style.WARNING(f'⚠️ ناموفق: {failed} دوره'))
        self.stdout.write(self.style.SUCCESS('='*50))