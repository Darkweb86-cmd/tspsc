from django.urls import path
from . import views
app_name="exam"
urlpatterns = [
    path('add-questions/', views.add_questions, name='add_questions'),
    path('create-paper/', views.create_paper, name='create_paper'),
    path('create-concept/', views.create_concept, name='create_concept'),
    path('create-question/', views.create_question, name='create_question'),
    path('questiontype/add/',views.create_question_type,name='create_question_type'),
    path('questiontype/list/',views.questiontype_list,name='question_type_list'),
    # path('paper/<int:paper_id>/', views.paper_concepts, name='paper_concepts'),
    path('questions/',views.question_list,name='question_list'),
    # path('mcqs/',views.mcq_list,name='mcq_list'),
    path('concept/<int:concept_id>/', views.concept_questions, name='concept_questions'),

      # Paper pages
    path('paper/<int:paper_id>/', views.paper_detail, name='paper_detail'),

    # Concept questions
    path('concepts/', views.concept_sidebar_view, name='concept_sidebar'),
    path('update-attempts/', views.save_attempt, name='update_attempts'),
    path('concept/<int:concept_id>/questions/', views.concept_questions, name='concept_questions'),

    path('dashboard/',views.exam_dashboard,name='dashboard')
]
