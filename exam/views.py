import json
from django.shortcuts import render
from django.http import JsonResponse
from .models import *
from .forms import *


def add_questions(request):
    if request.method == "POST":
        try:
            paper_id = request.POST.get("paper")
            concept_id = request.POST.get("concept")
            type_id = request.POST.get("question_type")
            json_data = request.POST.get("json_data")

            questions = json.loads(json_data)

            for q in questions:
                Question.objects.create(
                    paper_id=paper_id,
                    concept_id=concept_id,
                    question_type_id=type_id,
                    question_text=q["question"],
                    data=q.get("data", {}),
                    correct_answer=q.get("answer", "")
                )

            return JsonResponse({"status": "success"})

        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)})

    papers = Paper.objects.all()
    concepts = Concept.objects.all()
    types = QuestionType.objects.all()

    return render(request, "exam/add_questions.html", {
        "papers": papers,
        "concepts": concepts,
        "types": types
    })





from django.shortcuts import render, get_object_or_404
from .models import Paper

def paper_concepts(request, paper_id):
    paper = get_object_or_404(Paper, id=paper_id)
    
    # Fetch concepts + questions
    concepts = paper.concepts.prefetch_related('questions').all()

    return render(request, "exam/paper_concept.html", {
        "paper": paper,
        "concepts": concepts
    })




def paperwiseconcepts(request, paper_id):
    paper = get_object_or_404(Paper, id=paper_id)
    concepts = paper.concepts.prefetch_related('questions')

    if paper_id == 1:
        template = "exam/paper1concept.html"
    elif paper_id == 2:
        template = "exam/paper2concept.html"
    else:
        template = "exam/paper3_concept.html"

    return render(request, template, {
        "paper": paper,
        "concepts": concepts
    })

from django.shortcuts import render
from .models import Question


def question_list(request,concept_id):
    questions = Question.objects.all()

    return render(request, "exam/question_list.html", {
        "questions": questions
    })
import json
from django.http import JsonResponse
from .models import Question


def save_question(request):
    if request.method == "POST":
        question_type = request.POST.get("question_type")
        json_data = request.POST.get("json_data")

        Question.objects.create(
            question_type=question_type,
            question_data=json.loads(json_data)
        )

        return JsonResponse({"status": "saved"})
    
from django.shortcuts import render, get_object_or_404
from .models import Paper, Concept


from django.shortcuts import render, get_object_or_404
from .models import Paper, Concept


def paper_concepts(request, paper_id):
    paper = get_object_or_404(Paper, id=paper_id)
    concepts = paper.concepts.all()

    return render(request, "exam/paper_concepts.html", {
        "paper": paper,
        "concepts": concepts
    })


def concept_questions(request, concept_id):
    concept = get_object_or_404(Concept, id=concept_id)

    questions = concept.questions.all()

    return render(request, "exam/concept_questions.html", {
        "concept": concept,
        "questions": questions
    })


from django.shortcuts import render, redirect
from .forms import PaperForm, ConceptForm, QuestionForm
from .models import Paper, Concept


def create_paper(request):
    form = PaperForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('exam:create_paper')

    return render(request, "exam/create_paper.html", {"form": form})


def create_concept(request):
    form = ConceptForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('exam:create_concept')

    return render(request, "exam/create_concept.html", {"form": form})

from django.shortcuts import render, redirect, get_object_or_404
from .models import Paper, Concept, QuestionType, Question
import json

def create_question(request,concept_id=None):
    """
    Create a new question.
    - Paper and Concept selected from dropdown.
    - QuestionType selected.
    - JSON input for all question types.
    """
  
    # Fetch all papers, concepts, question types for dropdown
    papers = Paper.objects.all().order_by("id")
    concepts = Concept.objects.select_related("paper").all().order_by("id")
    questiontypes = QuestionType.objects.all().order_by("id")
    selected_concept=None
    selected_paper=None
    if concept_id:
        selected_concept=get_object_or_404(Concept,id=concept_id,paper=papers)
        selected_paper=selected_concept.paper
    if request.method == "POST":
        paper_id = request.POST.get("paper") or ( selected_paper.id if selected_paper else None)
        concept_id_post = request.POST.get("concept") or ( selected_concept.id if selected_concept else None)
        questiontype_id = request.POST.get("questiontype")
        raw_json = request.POST.get("question_data")
        
        # Fetch single instances (must be single instances!)
        paper_instance = get_object_or_404(Paper, id=paper_id)
        concept_instance = get_object_or_404(Concept, id=concept_id_post)
        questiontype_instance = get_object_or_404(QuestionType, id=questiontype_id)

        # Create Question
        Question.objects.create(
            paper=paper_instance,
            concept=concept_instance,
            questiontype=questiontype_instance,
            question_data=json.loads(raw_json)
        )

        return redirect('exam:question_list')  # redirect to all questions list

    return render(request, "exam/create_question.html", {
        "papers": papers,
        "concepts": concepts,
        "questiontypes": questiontypes,
    })


def question_list(request,concept_id=None):
    """
    Display all questions paper-wise, concept-wise, type-wise
    """
    questions = Question.objects.select_related(
        "paper",
        "concept",
        "questiontype"
    ).all().order_by("-id")

    return render(request, "exam/questions_list.html", {
        "questions": questions
    })

# def question_list(request):
#     questions=Question.objects.select_related("questiontype",'concept','concept__paper').all().order('-id')
#     return render(request,'exam/questions_list.html',{"questions":questions})



def create_question_type(request):
    if request.method=='POST':
        form=QuestionTypeForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('question_type_list')
    else:
        form=QuestionTypeForm()
    return render(request,'exam/questiontype_form.html',{'form':form})

def questiontype_list(request):
    types=QuestionType.objects.all()
    return render(request,'exam/questiontype_list.html',{'types':types})


                  


                  
###################################
# display mcqlist 
# ########################## 
# def mcq_list(request):
#     mcqs=Question.objects.select_related("concept","concept__paper","questiontype").filter(questiontype__name="mcq").order_by('id')
#     return render('request','exam/mcq_list.html',{'mcqs':mcqs})



from django.shortcuts import render, get_object_or_404
from .models import Paper, Concept, Question

# Generic view for any paper
def paper_detail(request, paper_id):
    paper = get_object_or_404(Paper, id=paper_id)
    concepts = Concept.objects.filter(paper=paper).order_by('id')

    return render(request, "exam/paper_concepts.html", {
        "paper": paper,
        "concepts": concepts
    })

# View to display questions under a concept
def concept_questions(request, concept_id):
    concept = get_object_or_404(Concept, id=concept_id)
    questions = Question.objects.filter(concept=concept).select_related('questiontype').order_by('id')
   

    return render(request, "exam/concept_questions.html", {
        "concept": concept,
        "questions": questions
    })

from django.db.models import Count

def concept_sidebar_view(request):
    # This groups concepts by name and counts how many papers reference each name
    # concepts= Concept.objects.all().order_by('name')
    papers = Paper.objects.prefetch_related('concepts').all()
    return render(request, 'exam/list_concept.html', {
        'papers': papers
    })


import json
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
# 2. Save logic (Persists the data)
@csrf_exempt
def save_attempt(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            concept_id = data.get('id')
            new_count = data.get('attempts')
            
            concept = Concept.objects.get(id=concept_id)
            concept.attempts = new_count
            concept.save()
            
            return JsonResponse({'status': 'saved', 'value': concept.attempts})
        
        except Concept.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Concept not found'}, status=404)
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)

    # CRITICAL: This handles GET requests or other methods so the view never returns None
    return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=405)

def exam_dashboard(request):
    papers=Paper.objects.all()
    return render(request,'exam/exam_dashboard.html',{'papers':papers})