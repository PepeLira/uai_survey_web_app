from django import forms
from .models import Survey, SurveyCareer, Career, Dashboard, Query, QuerySurveyQuestion, Question, SurveyQuestion


class DateInput(forms.DateInput):
    input_type = 'date'


class SurveyModelForm(forms.ModelForm):
    class Meta:
        model = Survey
        fields = ('csv_file', 'category', 'faculty', 'description', 'start_date',)
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


class DashboardForm(forms.ModelForm):
    class Meta:
        model = Dashboard
        fields = ('name', 'description', 'period')

        labels = {
            'name': 'Titulo',
            'description': 'Descripción',
            'period': 'Periodo',
        }


class QueryForm(forms.ModelForm):
    class Meta:
        model = Query
        fields = ('name', 'description', 'graph_type', 'privilege')

        labels = {
            'name': 'Titulo',
            'description': 'Descripción',
            'graph_type': 'Tipo de Grafico',
            'privilege': 'Nivel de Acceso',
        }


class QuerySurveyQuestionForm(forms.ModelForm):
    survey = forms.ModelChoiceField(queryset=Survey.objects.all())
    question = forms.ModelChoiceField(queryset=Question.objects.all())

    class Meta:
        model = QuerySurveyQuestion
        fields = ['survey', 'question']

    def save(self, commit=True, query_id=None):
        instance = super(QuerySurveyQuestionForm, self).save(commit=False)
        _survey = self.cleaned_data.get('survey')
        _question = self.cleaned_data.get('question')
        obj_survey_question = SurveyQuestion.objects.get(survey=_survey, question=_question)
        instance.survey_question = obj_survey_question
        instance.query_id = query_id
        instance.save()

        return instance
