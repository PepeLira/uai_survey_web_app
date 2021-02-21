from django.contrib import admin
from .models import (Survey, Question, OfferedAnswer, Person, Answer, Query, Privileges,
                     Faculty, Career, SurveyCategory, QuestionCategory, SurveyCareer, Dashboard,
                     Period, QuerySurveyQuestion, DashboardQuery)

admin.site.register(Survey)
admin.site.register(Question)
admin.site.register(OfferedAnswer)
admin.site.register(Person)
admin.site.register(Answer)
admin.site.register(Query)
admin.site.register(Privileges)
admin.site.register(Faculty)
admin.site.register(Career)
admin.site.register(SurveyCategory)
admin.site.register(QuestionCategory)
admin.site.register(SurveyCareer)
admin.site.register(Dashboard)
admin.site.register(Period)
admin.site.register(QuerySurveyQuestion)
admin.site.register(DashboardQuery)
