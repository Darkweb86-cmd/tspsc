from django import forms
from .models import *
import json


class PaperForm(forms.ModelForm):
    class Meta:
        model = Paper
        fields = ['name']


class ConceptForm(forms.ModelForm):
    class Meta:
        model = Concept
        fields = ['paper', 'name','attempts']


class QuestionForm(forms.ModelForm):

    json_data = forms.CharField(widget=forms.Textarea)

    class Meta:
        model = Question
        fields = ['paper', 'concept', 'questiontype', 'json_data','question_text']

    def clean_json_data(self):
        data = self.cleaned_data['json_data']
        try:
            return json.loads(data)
        except:
            raise forms.ValidationError("Invalid JSON format")
        
class QuestionTypeForm(forms.ModelForm):
    class Meta:
        model=QuestionType
        fields=['name']

    