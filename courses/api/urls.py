from django.urls import path
from courses.views.course_views import (
    CourseListView, 
    CourseDetailView, 
    InstructorCourseListView, 
    InstructorCourseDetailView
)
from courses.views.enrollment_views import (
    EnrollCourseView, 
    CourseContentAccessView, 
    MyCoursesView
)
from courses.views.progress_views import UpdateVideoProgressView
from courses.views.section_views import SectionDetailView, SectionListView
from courses.views.video_views import VideoListView

app_name = 'courses'

urlpatterns = [
    # عمومی
    path('', CourseListView.as_view(), name='course_list'),
    path('<slug:slug>/', CourseDetailView.as_view(), name='course_detail'),
    
    # دسترسی به محتوا
    path('<slug:course_slug>/video/<int:video_id>/', 
         CourseContentAccessView.as_view(), 
         name='course_content'),
    
    # مدرس: مدیریت دوره‌ها
    path('instructor/courses/', 
         InstructorCourseListView.as_view(), 
         name='instructor_courses'),
    path('instructor/courses/<slug:slug>/', 
         InstructorCourseDetailView.as_view(), 
         name='instructor_course_detail'),
    
    # مدرس: مدیریت سکشن‌ها
    path('instructor/courses/<int:course_id>/sections/', 
         SectionListView.as_view(), 
         name='section_list'),
    path('instructor/sections/<int:pk>/', 
         SectionDetailView.as_view(), 
         name='section_detail'),
    
    # مدرس: مدیریت ویدیوها
    path('instructor/sections/<int:section_id>/videos/', 
         VideoListView.as_view(), 
         name='video_list'),
    
    # دانشجو: ثبت‌نام و دوره‌های من
    path('enroll/<int:course_id>/', 
         EnrollCourseView.as_view(), 
         name='enroll_course'),
    path('my-courses/', 
         MyCoursesView.as_view(), 
         name='my_courses'),
    
    # دانشجو: پیشرفت ویدیوها
    path('progress/<int:course_id>/video/<int:video_id>/', 
         UpdateVideoProgressView.as_view(), 
         name='update_progress'),
]