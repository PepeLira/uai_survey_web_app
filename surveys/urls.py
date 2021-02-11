from django.urls import path
from .models import Survey
from .views import load_careers, SurveyAddView, SurveysIndexView # get_csv_survey_file
from django.views.generic.dates import ArchiveIndexView

urlpatterns = [

 path('cargar/encuestas', SurveyAddView.as_view(), name='upload_csv'),
 path('ajax/load-careers/', load_careers, name='ajax_load_careers'),
 path('encuestas_disponibles/', SurveysIndexView.as_view(), name='surveys_index'),

]
