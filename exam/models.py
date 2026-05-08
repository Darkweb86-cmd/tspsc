from django.db import models

from django.db import models


class Paper(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Concept(models.Model):
    paper = models.ForeignKey(Paper, on_delete=models.CASCADE, related_name='concepts')
    name = models.CharField(max_length=200)
    attempts = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.paper.name} - {self.name}"


class QuestionType(models.Model):
    name = models.CharField(max_length=100)  # MCQ, MATCH, STATEMENT

    def __str__(self):
        return self.name


class Question(models.Model):
    TYPES_QUESTION = [
        ("MCQ", "MCQ"),
        ("MATCH", "Match the Following"),
        ("MULTI", "Multiple Statement"),
        ("CORRECT_INCORRECT", "Correct / Incorrect"),
        ("PAIR", "Correct / Incorrect Pair"),
        ("ASSERTION_REASON", "Assertion Reason"),
        ("ARRANGE", "Arrange the Following"),
        ("TRUE_FALSE_PATTERN", "True or Not Pattern"),
        ("WHICH_AMONG", "Which Among"),
    ]

    questiontype = models.ForeignKey(QuestionType, on_delete=models.CASCADE)
    question_type = models.CharField(max_length=30, choices=TYPES_QUESTION)
    created_at = models.DateTimeField(auto_now_add=True)

    # Store FULL JSON here
    question_data = models.JSONField()

    paper = models.ForeignKey(Paper, on_delete=models.CASCADE)
    concept = models.ForeignKey(Concept, on_delete=models.CASCADE)

    question_text = models.TextField()
    correct_answer = models.CharField(max_length=200)

  
    def __str__(self):
        return f"{self.question_type} - ID {self.id} - {self.question_text[:50]}"



 