from django.contrib import admin

# Register your models here.
from . import models 


# تعریف inline برای نمایش کامنت‌ها در صفحه دوره
class CommentInline(admin.TabularInline):  # یا میتونید از StackedInline استفاده کنید
    model = models.Comment
    extra = 0  # تعداد فرم‌های خالی اضافی
    fields = ['user', 'text', 'created_at']
    readonly_fields = ['created_at']  # فقط خواندنی
    can_delete = True
    show_change_link = True
    
    # اگر میخواید فقط کامنت‌های مربوط به همون دوره رو نشون بده
    # که خودکار انجام میشه چون foreign key تعریف کردید



@admin.register(models.Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ['pk', 'instructor', 'title', 'price', 'is_published']
    inlines = [CommentInline]

@admin.register(models.Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['pk', 'user', 'created_at']


@admin.register(models.Enrollment)
class CourseAdmin(admin.ModelAdmin):
    list_display = ['student', 'course', 'enrolled_at', 'is_completed']
@admin.register(models.Section)
class CourseAdmin(admin.ModelAdmin):
    list_display = ['course', 'title','order']
@admin.register(models.Video)
class CourseAdmin(admin.ModelAdmin):
    list_display = ['pk', 'section', 'title', 'duration', 'is_free', 'order', 'created_at']
@admin.register(models.VideoProgress)
class CourseAdmin(admin.ModelAdmin):
    list_display = ['enrollment', 'video', 'is_watched', 'last_position']

