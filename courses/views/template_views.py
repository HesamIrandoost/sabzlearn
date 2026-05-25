from django.shortcuts import render
from django.views.decorators.cache import cache_page


def course_list_view(request):
    """نمایش صفحه لیست دوره‌ها"""
    return render(request, 'courses/course_list.html')

def course_detail_view(request, course_slug):
    """نمایش صفحه جزئیات دوره"""
    return render(request, 'courses/course_detail.html', {'course_slug': course_slug})

@cache_page(60)
def video_player_view(request, course_slug, video_id):
    """نمایش صفحه پخش ویدیو"""
    return render(request, 'courses/video_player.html', {
        'course_slug': course_slug,
        'video_id': video_id
    })