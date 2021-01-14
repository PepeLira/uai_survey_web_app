from django.db import models


class Survey(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    upload_date = models.DateTimeField(auto_now_add=True)
    start_date = models.DateField()
    end_date = models.DateField()
    is_open = models.BooleanField(default=False)

    def __str__(self):
        return self.title


class Question(models.Model):
    question_text = models.CharField(max_length=300)

    def __str__(self):
        return self.question_text


class OfferedAnswer(models.Model):
    option_text = models.CharField(max_length=300)

    def __str__(self):
        return self.option_text


class SurveyQuestion(models.Model):
    survey = models.ForeignKey(Survey, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)

    class Meta:
        unique_together = (("survey", "question"),)

    def __str__(self):
        return self.survey, self.question


class SurveyQuestionAnswer(models.Model):
    survey = models.ForeignKey(Survey, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    offered_answer = models.ForeignKey(OfferedAnswer, on_delete=models.CASCADE)

    class Meta:
        unique_together = (("survey", "question", "offered_answer"),)

    def __str__(self):
        return self.survey, self.question, self.offered_answer


class Person(models.Model):
    rut = models.IntegerField()
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email_1 = models.EmailField()
    email_2 = models.EmailField()
    phone = models.IntegerField()

    def __str__(self):
        return self.first_name, self.last_name


class Answer(models.Model):
    survey = models.ForeignKey(Survey, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    offered_answer = models.ForeignKey(OfferedAnswer, on_delete=models.CASCADE)
    person = models.ForeignKey(Person, on_delete=models.CASCADE)
    answer_text = models.TextField(blank=True)

    class Meta:
        unique_together = (("survey", "question", "offered_answer", "person"),)

    def __str__(self):
        return self.offered_answer, self.answer_text


class Query(models.Model):
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class QuerySurvey(models.Model):
    survey = models.ForeignKey(Survey, on_delete=models.CASCADE)
    query = models.ForeignKey(Question, on_delete=models.CASCADE)

    class Meta:
        unique_together = (("survey", "query"),)

    def __str__(self):
        return self.survey, self.query


class Privileges(models.Model):
    EGRESADO = 'Egresado'
    EQUIPO_ALUMNI = 'Equipo Alumni'
    CLIENTE_INTERNO = 'Cliente Interno'

    AVAILABLE_PRIVILEGES = [
        (EGRESADO, 'Egresado'),
        (EQUIPO_ALUMNI, 'Equipo Alumni'),
        (CLIENTE_INTERNO, 'Cliente Interno'),
    ]
    type = models.CharField(max_length=30,
                            choices=AVAILABLE_PRIVILEGES,
                            default=EGRESADO)

    def __str__(self):
        return self.type


class PrivilegesQuery(models.Model):
    privileges = models.ForeignKey(Privileges, on_delete=models.CASCADE)
    query = models.ForeignKey(Question, on_delete=models.CASCADE)

    class Meta:
        unique_together = (("privileges", "query"),)

    def __str__(self):
        return self.privileges, self.query
