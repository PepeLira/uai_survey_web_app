from django.urls import path

from .views import load_careers, SurveyAddView # get_csv_survey_file

urlpatterns = [

 path('cargar/encuestas', SurveyAddView.as_view(), name='upload_csv'),
 path('ajax/load-careers/', load_careers, name='ajax_load_careers'),

]
