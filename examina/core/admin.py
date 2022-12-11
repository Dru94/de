from django.contrib import admin
from .models import Examiner, User, Test, Question, Answer
# Register your models here.
admin.site.register(Examiner)
admin.site.register(User)
admin.site.register(Test)
admin.site.register(Question)
admin.site.register(Answer)