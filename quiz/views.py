# quiz/views.py
from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.utils import timezone
from django.db.models import Count, Q
from .models import QuizCategory, Quiz, Question, QuizSession, UserAnswer, Choice
import json

def quiz_home(request):
    """Display all quiz categories and available quizzes"""
    categories = QuizCategory.objects.all().annotate(
        quiz_count=Count('quiz', filter=Q(quiz__is_active=True))
    )
    
    # Get featured quizzes (recent active quizzes)
    featured_quizzes = Quiz.objects.filter(is_active=True).order_by('-created_at')[:6]
    
    context = {
        'categories': categories,
        'featured_quizzes': featured_quizzes,
    }
    return render(request, 'quiz/quiz_home.html', context)

def category_quizzes(request, category_slug):
    """Display quizzes in a specific category"""
    category = get_object_or_404(QuizCategory, slug=category_slug)
    quizzes = Quiz.objects.filter(category=category, is_active=True)
    
    context = {
        'category': category,
        'quizzes': quizzes,
    }
    return render(request, 'quiz/category_quizzes.html', context)

def quiz_detail(request, quiz_slug):
    """Display quiz details and start quiz option"""
    quiz = get_object_or_404(Quiz, slug=quiz_slug, is_active=True)
    
    context = {
        'quiz': quiz,
    }
    return render(request, 'quiz/quiz_detail.html', context)

def start_quiz(request, quiz_slug):
    """Start a new quiz session"""
    quiz = get_object_or_404(Quiz, slug=quiz_slug, is_active=True)
    
    # Create a new quiz session
    session = QuizSession.objects.create(
        quiz=quiz,
        total_questions=quiz.questions.count()
    )
    
    return redirect('quiz:take_quiz', session_id=session.session_id)

def take_quiz(request, session_id):
    """Take the quiz - display questions one by one"""
    session = get_object_or_404(QuizSession, session_id=session_id, is_completed=False)
    
    # Get answered questions for this session
    answered_questions = UserAnswer.objects.filter(session=session).values_list('question_id', flat=True)
    
    # Get next unanswered question
    next_question = session.quiz.questions.exclude(id__in=answered_questions).first()
    
    if not next_question:
        # All questions answered, redirect to results
        return redirect('quiz:quiz_results', session_id=session_id)
    
    # Get current question number
    current_question_number = len(answered_questions) + 1
    
    context = {
        'session': session,
        'question': next_question,
        'current_question_number': current_question_number,
        'total_questions': session.total_questions,
        'progress_percentage': (current_question_number / session.total_questions) * 100,
    }
    return render(request, 'quiz/take_quiz.html', context)

@require_POST
def submit_answer(request, session_id):
    """Submit answer for current question"""
    session = get_object_or_404(QuizSession, session_id=session_id, is_completed=False)
    
    try:
        data = json.loads(request.body)
        question_id = data.get('question_id')
        choice_id = data.get('choice_id')
        
        question = get_object_or_404(Question, id=question_id, quiz=session.quiz)
        choice = get_object_or_404(Choice, id=choice_id, question=question)
        
        # Save user answer
        user_answer, created = UserAnswer.objects.get_or_create(
            session=session,
            question=question,
            defaults={'selected_choice': choice}
        )
        
        if not created:
            # Update existing answer
            user_answer.selected_choice = choice
            user_answer.is_correct = choice.is_correct
            user_answer.save()
        
        # Check if quiz is completed
        answered_count = UserAnswer.objects.filter(session=session).count()
        is_completed = answered_count >= session.total_questions
        
        if is_completed:
            # Calculate final score
            correct_answers = UserAnswer.objects.filter(session=session, is_correct=True).count()
            session.score = correct_answers
            session.is_completed = True
            session.completed_at = timezone.now()
            session.save()
        
        return JsonResponse({
            'success': True,
            'is_completed': is_completed,
            'redirect_url': f'/quiz/results/{session_id}/' if is_completed else f'/quiz/take/{session_id}/'
        })
        
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})

def quiz_results(request, session_id):
    """Display quiz results"""
    session = get_object_or_404(QuizSession, session_id=session_id, is_completed=True)
    
    # Get all answers with details
    answers = UserAnswer.objects.filter(session=session).select_related(
        'question', 'selected_choice'
    ).order_by('question__order')
    
    # Calculate statistics
    correct_answers = answers.filter(is_correct=True).count()
    incorrect_answers = answers.filter(is_correct=False).count()
    
    # Performance rating
    percentage = session.percentage_score
    if percentage >= 90:
        rating = "Excellent"
        rating_class = "success"
    elif percentage >= 75:
        rating = "Good"
        rating_class = "info"
    elif percentage >= 60:
        rating = "Average"
        rating_class = "warning"
    else:
        rating = "Needs Improvement"
        rating_class = "danger"
    
    context = {
        'session': session,
        'answers': answers,
        'correct_answers': correct_answers,
        'incorrect_answers': incorrect_answers,
        'percentage': percentage,
        'rating': rating,
        'rating_class': rating_class,
    }
    return render(request, 'quiz/quiz_results.html', context)

def review_answers(request, session_id):
    """Review all answers with explanations"""
    session = get_object_or_404(QuizSession, session_id=session_id, is_completed=True)
    
    # Get all answers with question details
    answers = UserAnswer.objects.filter(session=session).select_related(
        'question', 'selected_choice'
    ).prefetch_related('question__choices').order_by('question__order')
    
    # Prepare answer details with correct answers
    answer_details = []
    for answer in answers:
        correct_choice = answer.question.choices.filter(is_correct=True).first()
        answer_details.append({
            'question': answer.question,
            'selected_choice': answer.selected_choice,
            'correct_choice': correct_choice,
            'is_correct': answer.is_correct,
            'all_choices': answer.question.choices.all()
        })
    
    context = {
        'session': session,
        'answer_details': answer_details,
    }
    return render(request, 'quiz/review_answers.html', context)