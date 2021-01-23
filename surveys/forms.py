from django import forms
from .models import Survey

class DateInput(forms.DateInput):
    input_type = 'date'
class SurveyModelForm(forms.ModelForm):
    class Meta:
        model = Survey
        fields = ('facultad', 'description', 'start_date', 'is_open', 'csv_file',)
        widgets = {
            'start_date': DateInput,
        }
