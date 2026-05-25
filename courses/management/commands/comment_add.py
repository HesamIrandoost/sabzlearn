from django.core.management.base import BaseCommand
from faker import Faker
from random import randint
from courses.models import Course, Comment
from accounts.models import User

class Command(BaseCommand):
    help = 'insert persian comment data'
    all_course = Course.objects.all()
        
    def __init__(self, *args, **kwargs):
        super(Command, self).__init__(*args, **kwargs)
        self.fake = Faker('fa_IR')

    def handle(self, *args, **options):
        for i in range(10, 15):
            c_user = User.objects.get(pk=i)
            for t_c in self.all_course:
                Comment.objects.create(
                    user=c_user,
                    course=t_c,
                    text=self.fake.paragraph(nb_sentences=randint(5, 20))
                )



# x = Course.objects.get(slu(g="redis-3")


# class Comment(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     course = models.ForeignKey(Course, on_delete=models.CASCADE)
#     text = models.CharField(max_length=500)
#     created_at = models.DateTimeField(auto_now_add=True)
       
#     def __str__(self):
#         return f"{self.user}"
    