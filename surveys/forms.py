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
        fields = ('name', 'description', 'graph_type', 'privilege', 'percentage_values', 'include_nan')
        BAR = 'Bar Chart'
        COMPARATIVE_BAR = 'Comparative Bar Chart'
        PIE = 'Pie Chart'
        TABLE = 'Table'

        AVAILABLE_GRAPH_TYPES = [
            (BAR, 'Bar Chart'),
            (COMPARATIVE_BAR, 'Comparative Bar Chart'),
            (PIE, 'Pie Chart'),
            (TABLE, 'Table'),
        ]

        labels = {
            'name': 'Titulo',
            'description': 'Descripción',
            'graph_type': 'Tipo de Grafico',
            'privilege': 'Nivel de Acceso',
            'percentage_values': 'Valores en %',
            'include_nan': 'Incluir Respuestas Nulas'

        }

        widgets = {
            'name': forms.TextInput(attrs={'class': "form-control"}),
            'description': forms.Textarea(attrs={'class': "form-control", 'rows': "5", 'placeholder': "texto..."}),
            'graph_type': forms.RadioSelect(choices=AVAILABLE_GRAPH_TYPES, attrs={'class': "flat"}),
            'privilege': forms.RadioSelect(choices=AVAILABLE_GRAPH_TYPES, attrs={'class': "flat"}),
            'percentage_values': forms.CheckboxInput(attrs={'class': "flat"}),
            'include_nan': forms.CheckboxInput(attrs={'class': "flat"}),
        }


class QuerySurveyQuestionForm(forms.ModelForm):
    encuesta = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': "form-control", 'type': "text", 'list': "surveylist", 'placeholder': "Buscar Encuesta..."
            }))

    question_queryset = Question.objects.all()

    pregunta = forms.ModelChoiceField(queryset=question_queryset,
                                      widget=forms.Select(
                                          attrs={
                                              'class': "form-control"
                                          }))

    survey_queryset = Survey.objects.all()

    class Meta:
        model = QuerySurveyQuestion
        fields = ['encuesta', 'pregunta']

    def save(self, commit=True, query_id=None):
        instance = super(QuerySurveyQuestionForm, self).save(commit=False)
        _survey = self.cleaned_data.get('encuesta')
        _survey = int(_survey.split('.')[0])
        _question = self.cleaned_data.get('pregunta')
        obj_question = Question.objects.get(question_text=_question)
        obj_survey_question = SurveyQuestion.objects.get(survey=_survey, question=obj_question)
        instance.survey_question = obj_survey_question
        instance.query_id = query_id
        instance.save()

        return instance
