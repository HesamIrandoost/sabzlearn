from django.contrib import admin

# Register your models here.
from . import models 

@admin.register(models.Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ['pk', 'instructor', 'title', 'price', 'is_published']
@admin.register(models.Enrollment)
class CourseAdmin(admin.ModelAdmin):
    list_display = ['student', 'course', 'enrolled_at', 'is_completed']
@admin.register(models.Section)
class CourseAdmin(admin.ModelAdmin):
    list_display = ['course', 'title','order']
@admin.register(models.Video)
class CourseAdmin(admin.ModelAdmin):
    list_display = ['section', 'title', 'duration', 'is_free', 'order', 'created_at']
@admin.register(models.VideoProgress)
class CourseAdmin(admin.ModelAdmin):
    list_display = ['enrollment', 'video', 'is_watched', 'last_position']