from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.index, name='home'),
    path('register', views.RegisterExaminer.as_view(), name='regExaminer'),
    path('register-student', views.RegisterStudent.as_view(), name='regStudent'),
    path('dashboard', views.dashboard, name='dashboard'),
    path('add-test', views.createTest, name='createTest'),
    path('add-questions/<int:id>', views.createQuestionsView, name='createQuestions'),
    path('add-answer/<int:id>', views.createAnswerView, name='createAnswer'),
    path('view-test', views.viewTest, name='viewTest'),
    path('<int:id>/delete', views.deleteTestView, name="deleteTest"),
    path('start/<str:title>', views.TestStartView, name='testStart'),
    path('testing/<str:title>', views.testing, name='testing'),
    path('score', views.testSubmit, name='testSubmit'),
    path("login", views.loginView, name="login"),
    path("logout", views.logoutView, name= "logout"),
    path("update/<int:id>", views.updateTest, name="updateTest"),
    path("update/<int:id>", views.updateQuestion, name="updateQuestion"),
    path("profile/", views.profile, name="profile"),
    path('search/', views.searchView, name="search")
]
