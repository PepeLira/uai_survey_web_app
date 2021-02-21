from django.urls import path
from .models import Survey
from .views import (
 load_careers,
 SurveyAddView,
 SurveysIndexView,
 SurveyUpdateView,
 SurveyDelete,
 DashboardAddView,
 DashboardIndexView,
 DashboardDeleteView,
 DashboardDetailView,
 QueryAddView,
 DashboardView,
)

urlpatterns = [

 path('cargar/encuestas', SurveyAddView.as_view(), name='upload_csv'),
 path('ajax/load-careers/', load_careers, name='ajax_load_careers'),
 path('encuestas_disponibles/', SurveysIndexView.as_view(), name='surveys_index'),
 path('dashboard_disponibles/', DashboardIndexView.as_view(), name='dashboard_index'),
 path('survey/<int:pk>/edit/', SurveyUpdateView.as_view(), name='survey_edit'),
 path('survey/<int:pk>/delete/', SurveyDelete.as_view(), name='survey_delete'),
 path('dashboard/new/', DashboardAddView.as_view(), name='new_dashboard'),
 path('dashboard/<int:pk>/delete/', DashboardDeleteView.as_view(), name='dashboard_delete'),
 path('dashboard/<int:pk>', DashboardDetailView.as_view(), name='dashboard_detail'),
 path('dashboard/<int:pk>/query/new/', QueryAddView.as_view(), name='new_query'),
 path('dashboard/<int:pk>/template', DashboardView.as_view(), name='dashboard_template'),

]
