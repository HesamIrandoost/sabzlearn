from django.views import generic

class CourseView(generic.TemplateView):
    template_name = 'courses/course_view.html'