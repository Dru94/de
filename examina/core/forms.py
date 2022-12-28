from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, Examiner, Test, Question, Answer, Student


class ExaminerRegForm(UserCreationForm):
    institution = forms.CharField(max_length=200, required=False)
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    class Meta(UserCreationForm.Meta):
        model = User

    def save(self):
        user = super().save(commit=False)
        user.is_examiner = True
        user.is_student = False
        user.save()
        examiner = Examiner.objects.create(user=user)
        examiner.institution = self.cleaned_data['institution']
        examiner.first_name = self.cleaned_data['first_name']
        examiner.last_name = self.cleaned_data['last_name']
        examiner.save()

        return user

    
class studentRegForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    class Meta(UserCreationForm.Meta):
        model = User

    def save(self):
        user = super().save(commit=False)
        user.is_student = True
        user.is_examined = False
        user.save()
        student = Student.objects.create(user=user)
        student.first_name = self.cleaned_data['first_name']
        student.last_name = self.cleaned_data['last_name']
        student.save()

        return user
    

class TestForm(forms.ModelForm):
    class Meta:
        model=Test
        fields = ['description', 'duration', 'title', 'subject']

class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['question_text']
        
class AnswerForm(forms.ModelForm):
    class Meta:
        model = Answer
        fields = ['answer_text', 'correct']