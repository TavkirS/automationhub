 #quiz/admin.py
from django.contrib import admin
from .models import QuizCategory, Quiz, Question, Choice, QuizSession, UserAnswer

class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 4
    fields = ['choice_text', 'is_correct']

class QuestionInline(admin.StackedInline):
    model = Question
    extra = 0
    fields = ['question_text', 'explanation', 'order']

@admin.register(QuizCategory)
class QuizCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'created_at']
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ['name']

@admin.register(Quiz)
class QuizAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'total_questions', 'time_limit', 'is_active', 'created_at']
    list_filter = ['category', 'is_active', 'created_at']
    search_fields = ['title', 'description']
    prepopulated_fields = {'slug': ('title',)}
    inlines = [QuestionInline]
    
    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        # Update total questions count
        obj.total_questions = obj.questions.count()
        obj.save(update_fields=['total_questions'])

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'quiz', 'order', 'created_at']
    list_filter = ['quiz__category', 'quiz']
    search_fields = ['question_text', 'quiz__title']
    inlines = [ChoiceInline]
    
    def save_formset(self, request, form, formset, change):
        super().save_formset(request, form, formset, change)
        # Update quiz total questions count
        if hasattr(form.instance, 'quiz'):
            quiz = form.instance.quiz
            quiz.total_questions = quiz.questions.count()
            quiz.save(update_fields=['total_questions'])

@admin.register(Choice)
class ChoiceAdmin(admin.ModelAdmin):
    list_display = ['choice_text', 'question', 'is_correct']
    list_filter = ['is_correct', 'question__quiz__category']
    search_fields = ['choice_text', 'question__question_text']

@admin.register(QuizSession)
class QuizSessionAdmin(admin.ModelAdmin):
    list_display = ['session_id', 'quiz', 'score', 'total_questions', 'percentage_score', 'is_completed', 'started_at']
    list_filter = ['is_completed', 'quiz__category', 'started_at']
    search_fields = ['session_id', 'quiz__title']
    readonly_fields = ['session_id', 'started_at', 'percentage_score']
    
    def percentage_score(self, obj):
        return f"{obj.percentage_score}%"
    percentage_score.short_description = "Score %"

@admin.register(UserAnswer)
class UserAnswerAdmin(admin.ModelAdmin):
    list_display = ['session', 'question', 'selected_choice', 'is_correct', 'answered_at']
    list_filter = ['is_correct', 'session__quiz', 'answered_at']
    search_fields = ['session__session_id', 'question__question_text']
    readonly_fields = ['is_correct', 'answered_at']
