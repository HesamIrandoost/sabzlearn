from django.contrib import admin
from .models import Tag, Article

# Register your models here.

class TagInlines(admin.TabularInline):
    model = Tag
    extra = 0 
    fields = ['name']
    can_delete = True
    show_change_link = True
    

@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ['author', 'slug', 'title', 'image', 'created_at', 'updated_at']
    # inlines = [TagInlines]
    filter_horizontal = ['tags']

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ['name']

