from django.views.generic import TemplateView



class HomePageView(TemplateView):
    template_name = 'home.html'

class AdminMenuView(TemplateView):
    template_name = 'admin_menu.html'



