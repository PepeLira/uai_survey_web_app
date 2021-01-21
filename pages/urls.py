from django.urls import path

from .views import HomePageView, upload_csv

urlpatterns = [

path('', HomePageView.as_view(), name='home'),
path('upload/csv/', upload_csv, name='upload_csv'),

]
