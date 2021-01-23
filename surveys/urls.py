from django.urls import path

from .views import get_csv_survey_file

urlpatterns = [

 path('cargar/encuestas', get_csv_survey_file, name='upload_csv'),

]
