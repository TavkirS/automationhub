
# quiz/urls.py
from django.urls import path
from . import views

app_name = 'quiz'

urlpatterns = [
    # Quiz home page
    path('', views.quiz_home, name='home'),
    
    # Category-specific quizzes
    path('category/<slug:category_slug>/', views.category_quizzes, name='category_quizzes'),
    
    # Quiz detail and start
    path('<slug:quiz_slug>/', views.quiz_detail, name='quiz_detail'),
    path('<slug:quiz_slug>/start/', views.start_quiz, name='start_quiz'),
    
    # Taking quiz
    path('take/<uuid:session_id>/', views.take_quiz, name='take_quiz'),
    path('submit/<uuid:session_id>/', views.submit_answer, name='submit_answer'),
    
    # Results and review
    path('results/<uuid:session_id>/', views.quiz_results, name='quiz_results'),
    path('review/<uuid:session_id>/', views.review_answers, name='review_answers'),
]