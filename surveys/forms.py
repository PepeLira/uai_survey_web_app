from django import forms
from .models import Survey


class DateInput(forms.DateInput):
    input_type = 'date'


class SurveyModelForm(forms.ModelForm):
    class Meta:
        model = Survey
        fields = ('csv_file', 'facultad', 'description', 'start_date', )
        widgets = {
            'start_date': DateInput,
        }
