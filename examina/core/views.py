from django.shortcuts import render, redirect
from django.contrib.auth import login, logout 
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, authenticate
from django.contrib import messages
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
        return redirect('dashboard')

def dashboard(request):
    testArr = []
    examiner = Examiner.objects.get(user=request.user)
    test = Test.objects.filter(examiner=examiner)
    name = examiner.first_name + " " + examiner.last_name
    
    for t in test:
        testArr.append(t)
    context = {
        'name':name,
        'tests':testArr
    }
    return render(request, 'core/dashboard.html', context)

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
    test_id = qn.test.id
    ansArr = []
    print("??????",test_id)
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
        'answers':ansArr,
        'test_id':test_id
    }
    return render(request, 'test/answer.html', context)

def viewTest(request):
    context = {
        'questions':[]
    }
    examiner = Examiner.objects.get(user=request.user)
    testObj = Test.objects.filter(examiner=examiner).last()
    questionsObj = Question.objects.filter(test__title=testObj.title)
    for t in questionsObj:
        answersObj = Answer.objects.filter(question__question_text=t.question_text)
        cArr = []
        for a in answersObj:
            cArr.append(a)
        
        context['questions'].append({t:cArr})
    context["title"] = testObj.title
    context["duration"] = testObj.duration
    context["description"] = testObj.description
    context["testID"] = testObj.id

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
    
    questions = Question.objects.filter(test__title=title)
    for q in questions:
        dArr = []
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

def loginView(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():

            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                
                messages.info(request, f"You are now logged in as {username}.")
                return redirect("dashboard")
            else:
                messages.error(request,"Invalid username or password.")
        else:
            messages.error(request,"Invalid username or password.")
    form = AuthenticationForm()
    return render(request=request, template_name="auth/login.html", context={"form":form})

def logoutView(request):
	logout(request)
	messages.info(request, "You have successfully logged out.") 
	return redirect("home")

def updateTest(request, id):
    test = Test.objects.get( id=id)
    form = TestForm(instance=test)
    if request.method == 'POST':
        f = TestForm(request.POST, instance=test)
        if f.is_valid():
            f.save()
            return redirect('viewTest')

    
    context = {
        "form":form,
        "testID":test.id
    }
    return render(request, 'test/editTest.html', context)

def updateQuestion(request, id):
    question = Question.objects.get(id=id)
    print("<<<<<>>>>",question)
    form = QuestionForm(instance=question)
    if request.method == 'POST':
        f = QuestionForm(request.POST, instance=question)
        if f.is_valid():
            f.save()
            return redirect('viewTest')

    
    context = {
        "form":form,
        "testID":question.id
    }
    return render(request, 'test/editQuestion.html', context)