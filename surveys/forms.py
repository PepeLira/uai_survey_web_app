from django import forms
from .models import Survey, SurveyCareer, Career



class DateInput(forms.DateInput):
    input_type = 'date'


class SurveyModelForm(forms.ModelForm):
    class Meta:
        model = Survey
        fields = ('csv_file', 'category', 'faculty', 'description', 'start_date', )
        widgets = {
            'start_date': DateInput,
        }
        labels = {
            'category': ('Categoría de la Encuesta'),
            'faculty': ('Facultad'),
            'description': ('Descripción'),
            'start_date': ('Fecha de Inicio'),
        }
        help_texts = {
            'start_date': ('La fecha en que comenzó la encuesta en SurveyMonkey'),
        }


class SurveyCareerForm(forms.ModelForm):
    class Meta:
        model = SurveyCareer
        fields = ('career',)

        labels = {
            'career': ('Carrera'),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['career'].queryset = SurveyCareer.objects.none()

        if 'faculty' in self.data:
            try:
                faculty_id = int(self.data.get('faculty'))
                self.fields['career'].queryset = Career.objects.filter(faculty_id=faculty_id).order_by('name')
            except (ValueError, TypeError):
                pass  # invalid input from the client; ignore and fallback to empty Career queryset
        elif self.instance.pk:
            self.fields['career'].queryset = self.instance.faculty.career_set.order_by('name')


SurveyCareerFormSet = forms.modelformset_factory(
    SurveyCareer, form=SurveyCareerForm, extra=1
)