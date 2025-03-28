from django import forms
from .itreporting.models import Student

class StudentProfileForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['photo', 'bio', 'group']
