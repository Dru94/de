from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.
class User(AbstractUser):
    is_student = models.BooleanField(default=False)
    is_examiner = models.BooleanField(default=False)
    
    
class Examiner(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    institution = models.CharField(max_length=200)
    first_name = models.CharField(max_length=30, null=True, default="")
    last_name = models.CharField(max_length=30, null=True, default="")
    
    def __str__(self) -> str:
        return self.user.username + " " + self.institution
    

class Test(models.Model):
    examiner = models.ForeignKey(Examiner, on_delete=models.CASCADE)
    duration = models.PositiveIntegerField()
    title = models.CharField(max_length=200)
    description = models.TextField(max_length=300)
    def __str__(self) -> str:
        return self.title + " " + self.description + " " + str(self.duration) + " " + self.examiner.first_name
    

class Question(models.Model):
    test = models.ForeignKey(Test, on_delete=models.CASCADE)
    question_text = models.CharField(max_length=200, blank=False)

    def __str__(self) -> str:
        return self.question_text
    
    
class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    answer_text = models.CharField(max_length=100, blank=False)
    correct = models.BooleanField(default=False)
    
    def __str__(self) -> str:
        return self.answer_text + " " + str(self.correct)
    
    
    