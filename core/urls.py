# core/urls.py
from django.contrib import admin
from django.urls import path, include
from rest_framework import permissions
from django.conf.urls.static import static
from django.conf import settings
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions


schema_view = get_schema_view(
    openapi.Info(
        title="SabzLearn API",
        default_version='v1',
        description="مستندات API سایت آموزشی سبزلرن",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@sabzlearn.local"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)    

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/account/', include('accounts.api.urls')),
    path('api/course/', include('courses.api.urls')),

    path('', include('courses.urls')),


    path('api-auth/', include('rest_framework.urls')),  # برای تست در براوزر
    # Swagger UI
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    
    # ReDoc UI
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    
    # JSON Schema
    path('swagger.json/', schema_view.without_ui(cache_timeout=0), name='schema-json'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)