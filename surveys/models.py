from django.db import models
from .validators import validate_csv_file_extension


class Faculty(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Career(models.Model):
    name = models.CharField(max_length=100)
    faculty = models.ForeignKey(Faculty, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class SurveyCategory(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Period(models.Model):
    name = models.CharField(max_length=150)

    def __str__(self):
        return self.name


class Survey(models.Model):
    title = models.CharField(max_length=100)
    # subtitle = models.CharField(max_length=100, blank=True)
    faculty = models.ForeignKey(Faculty, on_delete=models.CASCADE)
    category = models.ForeignKey(SurveyCategory, on_delete=models.CASCADE)
    description = models.TextField(max_length=300, blank=True)
    upload_date = models.DateTimeField(auto_now_add=True)
    start_date = models.DateField()
    is_activated = models.BooleanField(default=False)
    csv_file = models.FileField(upload_to='surveys_csvs/', validators=[validate_csv_file_extension])

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.title = f'Encuesta {self.faculty} - {self.start_date}'
        super().save(*args, **kwargs)


class SurveyCareer(models.Model):
    survey = models.ForeignKey(Survey, on_delete=models.CASCADE)
    career = models.ForeignKey(Career, on_delete=models.CASCADE)

    class Meta:
        unique_together = (("survey", "career"),)

    def __str__(self):
        template = f'{self.survey} {self.career}'
        return template.format(self)


class Question(models.Model):
    question_text = models.CharField(max_length=300, unique=True)
    type = models.CharField(max_length=300)

    def __str__(self):
        return self.question_text


class OfferedAnswer(models.Model):
    option_text = models.CharField(max_length=300, unique=True)

    def __str__(self):
        return self.option_text


class SurveyQuestion(models.Model):
    survey = models.ForeignKey(Survey, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)

    class Meta:
        unique_together = (("survey", "question"),)

    def __str__(self):
        template = f'{self.survey} {self.question}'
        return template.format(self)


class SurveyQuestionAnswer(models.Model):
    survey_question = models.ForeignKey(SurveyQuestion, on_delete=models.CASCADE)
    offered_answer = models.ForeignKey(OfferedAnswer, on_delete=models.CASCADE)

    class Meta:
        unique_together = (("survey_question", "offered_answer"),)

    def __str__(self):
        template = f'{self.survey_question} {self.offered_answer}'
        return template.format(self)


class Person(models.Model):
    rut = models.CharField(max_length=15, blank=True)
    nombres = models.CharField(max_length=255, blank=True)
    apellido_paterno = models.CharField(max_length=255, blank=True)
    apellido_materno = models.CharField(max_length=255, blank=True)
    email = models.EmailField(blank=True)
    phone = models.IntegerField(blank=True)

    def __str__(self):
        template = f'{self.nombres} {self.apellido_paterno} {self.apellido_materno}'
        return template.format(self)


class Answer(models.Model):
    survey_question_answer = models.ForeignKey(SurveyQuestionAnswer, on_delete=models.CASCADE)
    person = models.ForeignKey(Person, on_delete=models.CASCADE)
    answer_text = models.TextField(blank=True)

    def __str__(self):
        template = f'{self.survey_question_answer} {self.answer_text}'
        return template.format(self)


class Privileges(models.Model):
    EGRESADO = 1
    EQUIPO_ALUMNI = 3
    CORPORATIVO_UAI = 2

    AVAILABLE_PRIVILEGES = [
        (EGRESADO, 'Egresado'),
        (EQUIPO_ALUMNI, 'Equipo Alumni'),
        (CORPORATIVO_UAI, 'Corporativo UAI'),
    ]
    type = models.IntegerField(choices=AVAILABLE_PRIVILEGES,
                               default=EGRESADO, unique=True)

    def __str__(self):
        return self.AVAILABLE_PRIVILEGES[self.type - 1][1]


class Query(models.Model):
    BAR = 'Bar_Chart'
    COMPARATIVE_BAR = 'Comparative_Bar_Chart'
    PIE = 'Pie_Chart'
    TABLE = 'Table'

    AVAILABLE_GRAPH_TYPES = [
        (BAR, 'Bar Chart'),
        (COMPARATIVE_BAR, 'Comparative Bar Chart'),
        (PIE, 'Pie Chart'),
        (TABLE, 'Table'),
    ]

    name = models.CharField(max_length=150)
    description = models.TextField(max_length=300)
    graph_type = models.CharField(max_length=300, choices=AVAILABLE_GRAPH_TYPES, default='Table')
    privilege = models.ForeignKey(Privileges, on_delete=models.CASCADE, default=1)
    percentage_values = models.BooleanField(default=False)
    include_nan = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class QuerySurveyQuestion(models.Model):
    survey_question = models.ForeignKey(SurveyQuestion, on_delete=models.CASCADE)
    query = models.ForeignKey(Query, on_delete=models.CASCADE)

    class Meta:
        unique_together = (("survey_question", "query"),)

    def __str__(self):
        template = f'{self.survey_question} {self.query}'
        return template.format(self)


class EquivalentQuestion(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='question')
    eq_question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='eq_question')

    class Meta:
        unique_together = (("question", "eq_question"),)

    def __str__(self):
        template = f'{self.question} {self.eq_question}'
        return template.format(self)


class Dashboard(models.Model):
    name = models.CharField(max_length=150)
    description = models.TextField(max_length=300, blank=True)
    period = models.ForeignKey(Period, on_delete=models.SET_NULL, blank=True, related_name='period', null=True)
    upload_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class DashboardQuery(models.Model):
    dashboard = models.ForeignKey(Dashboard, on_delete=models.CASCADE)
    query = models.ForeignKey(Query, on_delete=models.CASCADE)

    class Meta:
        unique_together = (("dashboard", "query"),)

    def __str__(self):
        template = f'{self.dashboard} {self.query}'
        return template.format(self)


class QuestionCategory(models.Model):
    name = models.CharField(max_length=150, unique=True)

    def __str__(self):
        return self.name


class QuestionQuestionCategory(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    category = models.ForeignKey(QuestionCategory, on_delete=models.CASCADE)

    class Meta:
        unique_together = (("question", "category"),)

    def __str__(self):
        template = f'{self.question} {self.category}'
        return template.format(self)
