from django.db import models
from accounts.models import InstructorProfile
from django.utils.text import slugify
import uuid

# Create your models here.


class Tag(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name
    

class Article(models.Model):
    author = models.ForeignKey(InstructorProfile, on_delete=models.CASCADE, related_name="articles")
    tags = models.ManyToManyField(Tag, related_name="articles",blank=True)
    slug = models.SlugField(max_length=60, unique=True, blank=True, editable=False)
    title = models.CharField(max_length=50)
    content = models.TextField()
    image = models.ImageField(upload_to="articles", blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = str(uuid.uuid4())[:8]  # فقط 8 کاراکتر اول
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title[:10]
