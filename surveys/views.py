from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.contrib import messages
from .models import Survey
import csv

from .forms import SurveyModelForm


# Create your views here.
def get_csv_survey_file(request):
    form = SurveyModelForm(request.POST or None, request.FILES or None)

    if form.is_valid():
        form.save()
        form = SurveyModelForm()
        obj = Survey.objects.get(is_open=False)
        # with open(obj.csv_file.path, 'r') as f:
        #     reader = csv.reader(f)
        #     print(reader)

        # csv_file = request.FILES.get("csv_file")
        #
        # if not csv_file.name.endswith('.csv'):
        #     messages.error(request, 'File is not CSV type')
        #     return HttpResponseRedirect(reverse("upload_csv"))

    return render(request, "upload_csv.html", {'form': form})
