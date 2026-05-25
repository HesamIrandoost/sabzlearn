from django.core.management.base import BaseCommand
from faker import Faker
from random import randint
from ...models import Tag

class Command(BaseCommand):
    help = 'insert persian tags data'
    

    def __init__(self, *args, **kwargs):
        super(Command, self).__init__(*args, **kwargs)
        self.fake = Faker('fa_IR')
        self.pre_tags = [
            'python', 'java script', 'php', 'html & css',
            'django', 'react', 'vue', 'laravel', 
            'git', 'docker', ' linux'
        ]

    def handle(self, *args, **options):
        for i in self.pre_tags:
            Tag.objects.create(
                name=i
            )


# x = Course.objects.get(slu(g="redis-3")


# class Comment(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     course = models.ForeignKey(Course, on_delete=models.CASCADE)
#     text = models.CharField(max_length=500)
#     created_at = models.DateTimeField(auto_now_add=True)
       
#     def __str__(self):
#         return f"{self.user}"
    