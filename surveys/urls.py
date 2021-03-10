from django.urls import path
from .models import Survey
from .views import (
 load_careers,
 load_preguntas,
 SurveyAddView,
 SurveysIndexView,
 SurveyUpdateView,
 SurveyDelete,
 DashboardAddView,
 DashboardAdminIndexView,
 DashboardIndexView,
 DashboardDeleteView,
 DashboardDetailView,
 QueryAddView,
 DashboardView,
 ChartData,
 FacultyAdminIndexView,
 FacultyDetailView,
)

urlpatterns = [

 path('cargar/encuestas', SurveyAddView.as_view(), name='upload_csv'),
 path('ajax/load-careers/', load_careers, name='ajax_load_careers'),
 path('encuestas_disponibles/', SurveysIndexView.as_view(), name='surveys_index'),
 path('dashboard_disponibles_admin/', DashboardAdminIndexView.as_view(), name='dashboard_admin_index'),
 path('dashboard_disponibles/', DashboardIndexView.as_view(), name='dashboard_index'),
 path('survey/<int:pk>/edit/', SurveyUpdateView.as_view(), name='survey_edit'),
 path('survey/<int:pk>/delete/', SurveyDelete.as_view(), name='survey_delete'),
 path('dashboard/new/', DashboardAddView.as_view(), name='new_dashboard'),
 path('dashboard/<int:pk>/delete/', DashboardDeleteView.as_view(), name='dashboard_delete'),
 path('dashboard/<int:pk>', DashboardDetailView.as_view(), name='dashboard_detail'),
 path('dashboard/<int:pk>/query/new/', QueryAddView.as_view(), name='new_query'),
 path('ajax/load-preguntas/', load_preguntas, name='ajax_load_preguntas'),
 path('dashboard/<int:pk>/template', DashboardView.as_view(), name='dashboard_template'),
 path('api/chart/query/<int:pk>/data', ChartData.as_view(), name='chart_data'),
 path('facultades_disponibles_admin/', FacultyAdminIndexView.as_view(), name='faculty_admin_index'),
 path('facultad/<int:pk>', FacultyDetailView.as_view(), name='faculty_detail'),
]
