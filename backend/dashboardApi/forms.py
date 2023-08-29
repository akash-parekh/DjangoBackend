from django import forms
from .models import Document, Assignment

class DocForm(forms.ModelForm):
    class Meta:
        model = Assignment
        fields = [
            'status'
        ]