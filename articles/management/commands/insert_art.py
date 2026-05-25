from django.core.management.base import BaseCommand
from faker import Faker
from ...models import Tag, Article
from accounts.models import InstructorProfile
import random



class Command(BaseCommand):
    help = 'insert persian article data'

    titles_basic = [
    "آموزش کامل پایتون برای مبتدیان",
    "مقدمه‌ای بر برنامه‌نویسی شیءگرا در پایتون",
    "آموزش جنگو – ساخت وب‌اپلیکیشن حرفه‌ای",
    "یادگیری REST API با جنگو و DRF",
    "مفاهیم پایه دیتابیس‌های رابطه‌ای",
    "آموزش گیت و گیت‌هاب از صفر تا صد",
    "آشنایی با دستورات لینوکس برای برنامه‌نویسان",
    "برنامه‌نویسی فرانت‌اند با React.js",
    "مبانی جاوااسکریپت – حلقه‌ها و توابع",
    "آموزش HTML و CSS – ساخت اولین صفحه وب",
    ]
    titles_advanced = [
    "بهینه‌سازی کوئری‌ها در جنگو برای API‌های پرترافیک",
    "طراحی میکروسرویس‌ها با Django و Docker",
    "مدیریت کش و سیلیک در REST API",
    "آموزش GraphQL با پایتون و Django",
    "ساخت وب‌سرویس مقیاس‌پذیر با FastAPI",
    "معماری تمیز (Clean Architecture) در پروژه‌های پایتون",
    "اتصال جنگو به Elasticsearch برای جستجوی پیشرفته",
    "مدیریت هویت و احراز هویت با JWT در DRF",
    "آموزش Celery و Redis برای تسک‌های آسنکرون",
    "تست نویسی حرفه‌ایی در جنگو با Pytest",
    
    ]
    titles_tools = [
    "معرفی بهترین ابر IDE های برنامه‌نویسی",
    "مقایسه PostgreSQL و MySQL برای پروژه‌های جنگو",
    "آموزش کار با Docker و docker-compose در پروژه‌های پایتون",
    "نصب و تنظیم Nginx و Gunicorn برای دیپلوی جنگو",
    "آشنایی با Git Workflow و استراتژی‌های Branching",
    "ابزارهای مانیتورینگ سرور برای برنامه‌نویسان",
    "آموزش Postman – تست API های جنگو",
    "معرفی و نصب Redis به عنوان کش و بروکر",
    "کار با WebSocket در جنگو با استفاده از Django Channels",
    "آموزش GitHub Actions – CI/CD برای پروژه‌های پایتون",
    
    ]
    titles_architecture = [
    "اصول SOLID در برنامه‌نویسی پایتون",
    "الگوهای طراحی (Design Patterns) در جنگو",
    "تفاوت MVC و MVT در جنگو",
    "معماری لایه‌ای در پروژه‌های جنگو",
    "طراحی پایگاه داده برای پروژه‌های بزرگ",
    "مقیاس‌پذیری افقی در Django",
    "آشنایی با Event-Driven Architecture در پایتون",
    "چطور یک API تمیز و RESTful طراحی کنیم؟",
    "استفاده از Repository Pattern در جنگو",
    "معماری CQRS - چه زمانی و چطور؟",   
    ]
    titles_challenges = [
    "۱۰ اشتباه رایج در مدل‌نویسی جنگو",
    "باعث N+1 Problem در DRF نشوید!",
    "رفع مشکلات رایج در دیپلوی جنگو",
    "مدیریت Session و Authentication در API ها",
    "بهبود عملکرد (Performance) در کوئری‌های جنگو",
    "رفع خطای CORS در جنگو هنگام ارتباط با React",
    "مدیریت فایل‌های استاتیک در جنگو روی سرور",
    "چطور از SQL Injection در جنگو جلوگیری کنیم؟",
    "مشکلات امنیتی رایج در API های جنگو",
    "رفع خطای Circular Import در پروژه‌های جنگو",
]

    all_titles = (
        titles_basic + 
        titles_advanced + 
        titles_tools + 
        titles_architecture + 
        titles_challenges
    )
    def __init__(self, *args, **kwargs):
        super(Command, self).__init__(*args, **kwargs)
        self.fake = Faker('fa_IR')

        # tags.set(random_tags) 

    def handle(self, *args, **options):
        authors = InstructorProfile.objects.all()
        all_tags = list(Tag.objects.all())  
        article_count = 0
        
        for author in authors:
            for _ in range(3):  
                num_tags = random.randint(2, min(6, len(all_tags)))
                random_tags = random.sample(all_tags, num_tags)
                
                title = random.choice(self.all_titles)

                article = Article.objects.create(
                    author=author,
                    title=title, 
                    content=self.fake.paragraph(nb_sentences=75),
                )
                
                article.tags.set(random_tags)
                article_count += 1
                
