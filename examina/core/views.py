from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.views.generic import CreateView
from .forms import ExaminerRegForm, TestForm, QuestionForm, AnswerForm
from .models import User, Examiner, Test, Question, Answer
# Create your views here.

questionArray = []


def index(request):
    arr = []
    tests = Test.objects.all()
    for test in tests:
        arr.append(test)
    
    context = {
        "tests":arr
    }    
    return render(request, 'core/index.html', context)

class RegisterExaminer(CreateView):
    model = User
    form_class = ExaminerRegForm
    template_name = 'auth/regExaminer.html'

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'examiner'
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('home')

def dashboard(request):
    return render(request, 'core/dashboard.html')



def createTest(request):
    if request.method == 'POST':
        form = TestForm(request.POST)
        examiner = Examiner.objects.get(user=request.user)
        if form.is_valid:
            form.instance.examiner = examiner
            form.save()
            return redirect('createQuestions', form.instance.id)
            
    context = {
        'form':TestForm
    }
    return render(request, 'test/createTest.html', context)


def createQuestionsView(request, id):
    if request.method == 'POST':
        form = QuestionForm(request.POST)
        test = Test.objects.get(id=id)
        if form.is_valid:
            form.instance.test = test
            form.save()
            
            return redirect('createAnswer', form.instance.id)
    context = {
        'form':QuestionForm,
        'examinerID':id
    }

    return render(request, 'test/questions.html', context)

def createAnswerView(request, id):
    qn = Question.objects.get(id=id)
    ans = Answer.objects.filter(question=qn)
    ansArr = []
    if request.method == 'POST':
        form = AnswerForm(request.POST)
        if form.is_valid:
            form.instance.question = qn
            form.save()
            return redirect('createAnswer', id)
    if len(ans) != 0:
        for a in ans:
            ansArr.append(a)
    context = {
        'ansForm': AnswerForm,
        'question':qn.question_text,
        'questionID':qn.id,
        'answers':ansArr
    }
    return render(request, 'test/answer.html', context)

def viewTest(request):
    cArr = []
    context = {
        'questions':[]
    }
    examiner = Examiner.objects.get(user=request.user)
    testObj = Test.objects.filter(examiner=examiner).last()
    questionsObj = Question.objects.filter(test__title=testObj.title)
    for t in questionsObj:
        answersObj = Answer.objects.filter(question__question_text=t.question_text)
        for a in answersObj:
            cArr.append(a)
        
        context['questions'].append({t:cArr})
    
    return render(request, 'core/viewTest.html', context)


def TestStartView(request, title):
    test = Test.objects.filter(title=title)
    context = {

    }
    for t in test:
        context['test'] = t

    return render(request, 'test/testStart.html', context)



def testing(request,title):
    context = {
        'questions':[]
    }
    dArr = []
    questions = Question.objects.filter(test__title=title)
    for q in questions:
        answers = Answer.objects.filter(question__question_text = q.question_text)
        questionArray.append(q)
        for a in answers:
            dArr.append(a)
        
        context['questions'].append({q:dArr})
        

    return render(request, 'test/testing.html', context)


def testSubmit(request):
    totalMark = len(questionArray)
    if request.method == 'POST':
        mark = 0
        for question in questionArray:
            x = request.POST.get(str(question))
            if x == 'True':
                mark+=1

        questionArray.clear()
        context = {
            'mark':mark,
            'totalMark':totalMark
        }
        return render(request, 'test/score.html', context)