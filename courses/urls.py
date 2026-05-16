from django.urls import path
from .views.template_views import CourseView

urlpatterns = [
    path('', CourseView.as_view(), name='course-view'),
]