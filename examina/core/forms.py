from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, Examiner, Test, Question, Answer


class ExaminerRegForm(UserCreationForm):
    institution = forms.CharField(max_length=200, required=False)
    class Meta(UserCreationForm.Meta):
        model = User

    def save(self):
        user = super().save(commit=False)
        user.is_examiner = True
        user.save()
        examiner = Examiner.objects.create(user=user)
        examiner.institution = self.cleaned_data['institution']
        examiner.save()

        return user
    

class TestForm(forms.ModelForm):
    class Meta:
        model=Test
        fields = ['description', 'duration', 'title']

class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['question_text']
        
class AnswerForm(forms.ModelForm):
    class Meta:
        model = Answer
        fields = ['answer_text', 'correct']