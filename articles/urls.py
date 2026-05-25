from django.urls import path
from . import views


app_name = 'articles'



urlpatterns = [
    path('', views.ArticleAPIView.as_view(), name='article-list'),
    path('slug:<slug>/', views.ArticleDetailAPIView.as_view(), name='article-detial'),

    path('author/article/', views.InstructorArticleListView.as_view(), name='article-author'),
    path('author/article/slug:<slug>/', views.InstructorArticleURDView.as_view(), name='article-author-manage'),
]
