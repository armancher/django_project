from django.db import models
from django.urls import reverse
from django.contrib.auth import get_user_model
from users.models import User

class Tag(models.Model):
    name = models.CharField(max_length=50,verbose_name="نام تگ")

    def __str__(self):
        return self.name



class Question(models.Model):
    title = models.CharField(max_length=100,verbose_name="عنوان سوال ")
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE,verbose_name="کاربر ایجاد کننده‌ی سوال")
    upvoters = models.ManyToManyField(User, related_name='upvoted_questions',verbose_name=" افراد upvote کننده‌ی سوال")
    downvoters = models.ManyToManyField(User, related_name='downvoted_questions',verbose_name="افراد downvote کننده‌ی سوال")
    tags = models.ManyToManyField('questions.Tag',related_name="tags") #rechecek
    @property
    def votes(self):
        return self.upvoters.count()-self.downvoters.count()
  



class Answer(models.Model):
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    upvoters = models.ManyToManyField(User, related_name='upvoted_answers')
    downvoters = models.ManyToManyField(User, related_name='downvoted_answers')
    class Meta:
        ordering=[
            '-created_at' ,
        ]
    @property
    def votes(self):
        return self.upvoters.count() - self.downvoters.count()
