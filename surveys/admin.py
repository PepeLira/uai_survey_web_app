from django.contrib import admin
from .models import Survey, Question, OfferedAnswer, Person, Answer, Query, Privileges


admin.site.register(Survey)
admin.site.register(Question)
admin.site.register(OfferedAnswer)
admin.site.register(Person)
admin.site.register(Answer)
admin.site.register(Query)
admin.site.register(Privileges)
