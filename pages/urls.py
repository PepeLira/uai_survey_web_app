from django.urls import path

from .views import HomePageView, AdminMenuView

urlpatterns = [

path('', HomePageView.as_view(), name='home'),
path('admin_menu/', AdminMenuView.as_view(), name='admin_menu'),


]
