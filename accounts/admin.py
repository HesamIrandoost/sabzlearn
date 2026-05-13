from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from django.utils.html import format_html
from .models import User, StudentProfile, InstructorProfile

class StudentProfileInline(admin.StackedInline):
    model = StudentProfile
    can_delete = False
    verbose_name_plural = 'پروفایل دانشجویی'
    fields = ('wallet_balance',)

class InstructorProfileInline(admin.StackedInline):
    model = InstructorProfile
    can_delete = False
    verbose_name_plural = 'پروفایل مدرس'
    fields = ('profile_image', 'bio', 'is_verified', 'total_students', 'total_courses')

class CustomUserAdmin(UserAdmin):
    list_display = ('phone', 'email', 'role_badge', 'is_instructor_approved', 'is_staff_badge', 'date_joined')
    list_filter = ('role', 'is_instructor_approved', 'is_staff', 'is_superuser', 'is_active')
    search_fields = ('phone', 'email')
    ordering = ('-date_joined',)
    
    fieldsets = (
        (None, {'fields': ('phone', 'password')}),
        ('اطلاعات شخصی', {'fields': ('email',)}),
        ('نقش و دسترسی‌ها', {
            'fields': ('role', 'is_instructor_approved', 'is_active', 'is_staff', 'is_superuser'),
            'classes': ('wide',)
        }),
        ('مجوزها', {
            'fields': ('groups', 'user_permissions'),
            'classes': ('collapse',)
        }),
    )
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('phone', 'email', 'password1', 'password2', 'role'),
        }),
    )
    
    def role_badge(self, obj):
        colors = {
            'student': 'blue',
            'instructor': 'green',
            'admin': 'orange'
        }
        return format_html(
            '<span style="background-color: {}; color: white; padding: 3px 8px; border-radius: 3px;">{}</span>',
            colors.get(obj.role, 'gray'),
            obj.get_role_display()
        )
    role_badge.short_description = 'نقش'
    role_badge.admin_order_field = 'role'
    
    def is_staff_badge(self, obj):
        if obj.is_staff:
            return format_html(
                '<span style="background-color: #417690; color: white; padding: 3px 8px; border-radius: 3px;">{}</span>',
                'ادمین'
            )
        else:
            return format_html(
                '<span style="background-color: #666; color: white; padding: 3px 8px; border-radius: 3px;">{}</span>',
                'کاربر عادی'
            )
    is_staff_badge.short_description = 'وضعیت ادمین'
    
    def get_inline_instances(self, request, obj=None):
        if not obj:
            return []
        
        inlines = []
        if obj.role == 'student':
            inlines.append(StudentProfileInline(self.model, self.admin_site))
        elif obj.role == 'instructor':
            inlines.append(InstructorProfileInline(self.model, self.admin_site))
        
        return inlines

# ثبت مدل‌ها در ادمین
admin.site.register(User, CustomUserAdmin)

@admin.register(StudentProfile)
class StudentProfileAdmin(admin.ModelAdmin):
    list_display = ('pk','user', 'wallet_balance')
    search_fields = ('user__phone',)
    list_filter = ('wallet_balance',)
    
@admin.register(InstructorProfile)
class InstructorProfileAdmin(admin.ModelAdmin):
    list_display = ('pk','user', 'is_verified', 'total_courses', 'total_students')
    list_filter = ('is_verified',)
    search_fields = ('user__phone', 'bio')
    list_editable = ('is_verified',)