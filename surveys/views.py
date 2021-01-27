from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.contrib import messages
from .models import Survey
import pandas as pd

from .forms import SurveyModelForm


def get_answer_type(df,column):
    # detecta todos los tipos excepto preguntas de selección multiple
    try:
        unique_answers = df[column][2:].describe()['unique']
        count_answers = df[column][2:].describe()['count']
        if unique_answers == 2:
            return 'Binary'
        elif unique_answers < count_answers*0.8:
            return 'Dropdown questions'
        else:
            return 'Open-Ended Text Response'
    except:
        return 'blank'


def create_models_from_csv(df):
    questions_df = pd.DataFrame(columns=['question', 'type'])
    # Primero se extraen las preguntas y sus tipos
    first_row_is_question = False
    for column in df.columns:
        first_cell = df.loc[0, column]
        second_cell = df.loc[1, column]
        if (not pd.isna(first_cell)) and pd.isna(second_cell):
            questions_df = questions_df.append(
                pd.DataFrame({'question': [first_cell], 'type': ['Open-Ended Text Response']}), ignore_index=True)
            # La primera fila es pregunta de texto.
        elif (not pd.isna(first_cell)) and (not pd.isna(second_cell)):
            if 'Response' == second_cell:
                questions_df = questions_df.append(
                    pd.DataFrame({'question': [first_cell], 'type': ['Dropdown questions']}), ignore_index=True)
                # La primera es pregunta de alternativas
                first_row_is_question = True
            elif 'Open-Ended Response' == second_cell:
                questions_df = questions_df.append(
                    pd.DataFrame({'question': [first_cell], 'type': ['Open-Ended Text Response']}), ignore_index=True)
                # La primera es pregunta de texto
            elif get_answer_type(df, column) == 'Binary':
                questions_df = questions_df.append(
                    pd.DataFrame({'question': [first_cell],
                                  'type': ['Multiple choice questions'],
                                  'choice': [second_cell]}), ignore_index=True)
                # La primera es pregunta de seleccion multiple, la segunda es una respuesta
                first_row_is_question = True
            else:
                questions_df = questions_df.append(
                    pd.DataFrame({'question': [second_cell], 'type': ['Open-Ended Text Response']}), ignore_index=True)
                # La segunda es pregunta de texto
                first_row_is_question = False
        elif first_row_is_question:
            if get_answer_type(df, column) == 'binary':
                questions_df = questions_df.append(
                    pd.DataFrame({'question': [df.loc[1, df.columns[-1]]],
                                  'type': ['Multiple choice questions'],
                                  'choice': [second_cell]}), ignore_index=True)
                # La segunda es RESPUESTA de Selección Multiple
            else:
                questions_df = questions_df.append(
                    pd.DataFrame({'question': [df.loc[1, df.columns[-1]]],
                                  'type': ['Multiple choice questions'],
                                  'choice': [second_cell]}), ignore_index=True)
                # La segunda es RESPUESTA alternativa de texto (Otro(especifique))
        # else:
        #     print()
        #     # La segunda es pregunta de texto
        #     first_row_is_question = False
    return questions_df


# Create your views here.
def get_csv_survey_file(request):
    form = SurveyModelForm(request.POST or None, request.FILES or None)

    if form.is_valid():
        form.save()
        form = SurveyModelForm()
        obj = Survey.objects.get(is_activated=False)

        survey_df = pd.read_csv(obj.csv_file.path, delimiter=',', encoding='utf8', header=None)

        print(create_models_from_csv(survey_df).to_string())

        obj.is_activated = True
        obj.save()

    return render(request, "upload_csv.html", {'form': form})
