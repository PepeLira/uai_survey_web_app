from django.views.generic import ListView, TemplateView, UpdateView, DeleteView, CreateView, DetailView
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse, reverse_lazy
from django.contrib import messages
from django.db.models import Count

from rest_framework.views import APIView
from rest_framework.response import Response

from .models import (Survey, Question, OfferedAnswer, SurveyQuestion,
                     SurveyQuestionAnswer, Person, Answer, EquivalentQuestion, SurveyCareer,
                     Career, QuestionCategory, QuestionQuestionCategory, Dashboard, DashboardQuery,
                     QuerySurveyQuestion, Faculty, Career)

from .forms import SurveyModelForm, SurveyCareerFormSet, DashboardForm, QueryForm, QuerySurveyQuestionForm

import pandas as pd


def load_careers(request):
    faculty = request.GET.get('faculty')
    careers = Career.objects.filter(faculty=faculty).order_by('name')
    return render(request, 'hr/career_dropdown_list_options.html', {'careers': careers})


def load_preguntas(request):
    survey = request.GET.get('encuesta')
    survey_question_objs = SurveyQuestion.objects.filter(survey=survey).order_by('question')
    return render(request, 'hr/question_dropdown_list_options.html', {'survey_question_objs': survey_question_objs})


def remove_survey_monkey_person_questions():
    list_questions2delete = ['respondent_id', 'collector_id', 'date_created', 'date_modified', 'ip_address',
                             'email_address', 'first_name', 'last_name', 'custom_1'
                             ]
    obj_question_category = QuestionCategory.objects.get(name='Datos Personales:')
    objs_question_question_category = QuestionQuestionCategory.objects.filter(category=obj_question_category)

    for obj in objs_question_question_category:
        list_questions2delete.append(obj.question.question_text)

    for q_text in list_questions2delete:
        Question.objects.get(question_text=q_text).delete()


class SurveyAddView(TemplateView):
    template_name = 'upload_csv.html'

    def detect_comma_or_dot_comma(self, file_path):
        csv_file_str = open(file_path, 'r', encoding='utf-8', errors='replace').read()
        n_dot_comma = csv_file_str.count(';')
        n_comma = csv_file_str.count(',')

        if n_dot_comma > n_comma:
            return ';'
        else:
            return ','

    def check_number_of_answers(self, df, column):
        count_answers = df[column][2:].describe()['count']
        return count_answers

    def only_numerics(self, str):
        seq_type = type(str)
        return seq_type().join(filter(seq_type.isdigit, str))

    def get_answer_type(self, df, column):
        # detecta todos los tipos excepto preguntas de selección multiple
        try:
            unique_answers = df[column][2:].describe()['unique']
            count_answers = df[column][2:].describe()['count']
            if unique_answers == 2:
                return 'Binary'
            elif unique_answers < count_answers * 0.8:
                return 'Dropdown questions'
            else:
                return 'Open-Ended Text Response'
        except:
            return 'blank'

    def clean_person(self, df, row, person_columns_list):
        rut = self.only_numerics(str(df[person_columns_list[3]][row]))
        valid = len(rut) > 5
        if valid:
            nombres = df[person_columns_list[0]][row]
            apellido_paterno = df[person_columns_list[1]][row]
            apellido_materno = df[person_columns_list[2]][row]
            rut = rut[:-1] + '-' + rut[-1]
            email = df[person_columns_list[4]][row]
            phone = self.only_numerics(df[person_columns_list[5]][row])
            person_list = [nombres, apellido_paterno, apellido_materno, rut, email, phone]
        else:
            person_list = []

        return person_list, valid

    def create_answers(self, df, question_df, person_columns_list, survey_obj):
        for row in df.index[2:]:
            # Create Person
            person_atr_list, valid = self.clean_person(df, row, person_columns_list)
            if valid:
                try:
                    person_obj, created = Person.objects.get_or_create(nombres=person_atr_list[0],
                                                                       apellido_paterno=person_atr_list[1],
                                                                       apellido_materno=person_atr_list[2],
                                                                       rut=person_atr_list[3],
                                                                       email=person_atr_list[4],
                                                                       phone=person_atr_list[5])
                    person_obj.save()
                except:
                    pass
            else:
                pass
            for column in question_df.index[person_columns_list[-1] + 1:]:
                question_text = question_df.question[column]
                question_obj = Question.objects.get(question_text=question_text)
                survey_question_obj = SurveyQuestion.objects.get(survey=survey_obj, question=question_obj)

                # Create Offered Answers with its SurveyQuestionAnswer relation
                answer_text = ''
                if question_df.choice[column] == 'Otro (especifique)':
                    answer_text = df[column][row]
                if question_df.type[column] == 'Dropdown questions':
                    o_answer = df[column][row]
                    if o_answer == '':
                        pass
                    offered_answer_obj, created = OfferedAnswer.objects.get_or_create(option_text=o_answer)
                    if created:
                        offered_answer_obj.save()
                    survey_question_answer_obj, created = SurveyQuestionAnswer.objects.get_or_create(
                        survey_question=survey_question_obj, offered_answer=offered_answer_obj)
                    if created:
                        survey_question_answer_obj.save()
                    answer_obj, created = Answer.objects.get_or_create(
                        survey_question_answer=survey_question_answer_obj,
                        person=person_obj, answer_text=answer_text)
                    if created:
                        answer_obj.save()
                    answer_text = ''

                elif question_df.type[column] == 'Multiple choice questions':
                    o_answer = question_df.choice[column]
                    offered_answer_obj, created = OfferedAnswer.objects.get_or_create(option_text=o_answer)
                    if created:
                        offered_answer_obj.save()
                    if df[column][row] == 'Sí':
                        survey_question_answer_obj, created = SurveyQuestionAnswer.objects.get_or_create(
                            survey_question=survey_question_obj, offered_answer=offered_answer_obj)
                        if created:
                            survey_question_answer_obj.save()
                        answer_obj, created = Answer.objects.get_or_create(
                            survey_question_answer=survey_question_answer_obj,
                            person=person_obj, answer_text=answer_text)
                        if created:
                            answer_obj.save()
                        answer_text = ''

                elif question_df.type[column] == 'Open-Ended Text Response':
                    o_answer = 'Open-Ended Text Response'
                    answer_text = df[column][row]
                    offered_answer_obj, created = OfferedAnswer.objects.get_or_create(option_text=o_answer)
                    if created:
                        offered_answer_obj.save()
                    survey_question_answer_obj, created = SurveyQuestionAnswer.objects.get_or_create(
                        survey_question=survey_question_obj, offered_answer=offered_answer_obj)
                    if created:
                        survey_question_answer_obj.save()
                    answer_obj, created = Answer.objects.get_or_create(
                        survey_question_answer=survey_question_answer_obj,
                        person=person_obj, answer_text=answer_text)
                    if created:
                        answer_obj.save()
                    answer_text = ''
                else:
                    pass

    def create_questions(self, question_df, survey_obj):
        # crea todos los objetos asociados a una misma pregunta.
        question_str = question_df.question.to_list()[-1]
        question_type = question_df.type.to_list()[-1]
        offered_answer = question_df.choice.to_list()[-1]
        category = question_df.category.to_list()[-1]

        # agregar, si existen, categorias de preguntas con sus preguntas y vinculos correspondientes
        if not pd.isna(category):
            question_category_obj, created = QuestionCategory.objects.get_or_create(name=category)
            if created:
                question_category_obj.save()
            question_obj, created = Question.objects.get_or_create(question_text=question_str, type=question_type)
            if created:
                question_obj.save()
            question_question_category_obj, created = \
                QuestionQuestionCategory.objects.get_or_create(question=question_obj, category=question_category_obj)
            if created:
                question_question_category_obj.save()
        else:
            # agregar preguntas
            question_obj, created = Question.objects.get_or_create(question_text=question_str, type=question_type)
            if created:
                question_obj.save()

        # agregar puente survey_question
        survey_question_obj, created = SurveyQuestion.objects.get_or_create(survey=survey_obj, question=question_obj)
        if created:
            survey_question_obj.save()



    def create_models_from_csv(self, df, survey_obj):
        questions_df = pd.DataFrame(columns=['question', 'type', 'choice', 'category'])
        person_columns_list = []
        # Primero se extraen las preguntas y sus tipos
        first_row_is_question = False
        for column in df.columns:
            first_cell = df.loc[0, column]
            second_cell = df.loc[1, column]
            if (not pd.isna(first_cell)) and pd.isna(second_cell):
                # La primera fila es pregunta de texto.
                questions_df = questions_df.append(
                    pd.DataFrame({'question': [first_cell], 'type': ['Open-Ended Text Response']}), ignore_index=True)

            elif (not pd.isna(first_cell)) and (not pd.isna(second_cell)):
                if 'Response' == second_cell:
                    # La primera es pregunta de alternativas
                    questions_df = questions_df.append(
                        pd.DataFrame({'question': [first_cell], 'type': ['Dropdown questions']}), ignore_index=True)

                    first_row_is_question = True
                elif 'Open-Ended Response' == second_cell:
                    # La primera es pregunta de texto
                    questions_df = questions_df.append(
                        pd.DataFrame({'question': [first_cell], 'type': ['Open-Ended Text Response']}),
                        ignore_index=True)

                elif self.get_answer_type(df, column) == 'Binary':
                    # La primera es pregunta de seleccion multiple, la segunda es una respuesta.
                    questions_df = questions_df.append(
                        pd.DataFrame({'question': [first_cell],
                                      'type': ['Multiple choice questions'],
                                      'choice': [second_cell]}), ignore_index=True)

                    first_row_is_question = True
                else:
                    # La segunda es pregunta de texto
                    questions_df = questions_df.append(
                        pd.DataFrame({'question': [second_cell],
                                      'type': ['Open-Ended Text Response'],
                                      'category': [first_cell]}), ignore_index=True)
                    category = first_cell
                    if category == 'Datos Personales:':
                        person_columns_list.append(column)
                    first_row_is_question = False
            elif first_row_is_question:
                if self.get_answer_type(df, column) == 'binary':
                    # La segunda es RESPUESTA de Selección Multiple
                    latest_question = questions_df.question.to_list()[-1]
                    questions_df = questions_df.append(
                        pd.DataFrame({'question': [latest_question],
                                      'type': ['Multiple choice questions'],
                                      'choice': [second_cell]}), ignore_index=True)
                else:
                    # La segunda es RESPUESTA alternativa de texto (Otro(especifique))
                    latest_question = questions_df.question.to_list()[-1]
                    latest_type = questions_df.type.to_list()[-1]
                    questions_df = questions_df.append(
                        pd.DataFrame({'question': [latest_question],
                                      'type': [latest_type],
                                      'choice': [second_cell]}), ignore_index=True)

            else:
                # La segunda es pregunta de texto
                questions_df = questions_df.append(
                    pd.DataFrame({'question': [second_cell],
                                  'type': ['Open-Ended Text Response'],
                                  'category': [category]}), ignore_index=True)
                if category == 'Datos Personales:':
                    person_columns_list.append(column)

                first_row_is_question = False
            self.create_questions(questions_df, survey_obj)
        return questions_df, person_columns_list

    def get(self, *args, **kwargs):
        survey_form = SurveyModelForm()
        formset = SurveyCareerFormSet(queryset=SurveyCareer.objects.none())

        return self.render_to_response({'survey_form': survey_form, 'survey_career_form_set': formset})

    def post(self, *args, **kwargs):
        survey_form = SurveyModelForm(self.request.POST or None, self.request.FILES or None)
        formset = SurveyCareerFormSet(data=self.request.POST)

        if survey_form.is_valid():
            survey_id = survey_form.save().pk
            if formset.is_valid():
                survey_career = formset.save(commit=False)
                for form in survey_career:
                    form.survey_id = survey_id
                    form.save()

                survey_obj = Survey.objects.get(is_activated=False)
                survey_obj.is_activated = True
                survey_obj.save()
                csv_file_path = survey_obj.csv_file.path
                survey_df = pd.read_csv(open(csv_file_path, encoding='utf-8', errors='replace'),
                                        delimiter=self.detect_comma_or_dot_comma(csv_file_path), encoding='utf8',
                                        header=None)

                question_df, person_column_list = self.create_models_from_csv(survey_df, survey_obj)
                self.create_answers(survey_df, question_df, person_column_list, survey_obj)
            return redirect(reverse_lazy("admin_menu"))
        remove_survey_monkey_person_questions()
        return self.render_to_response({'survey_form': survey_form, 'survey_career_form_set': formset})


class SurveysIndexView(ListView):
    model = Survey
    template_name = 'surveys_index.html'


class SurveyUpdateView(UpdateView):
    model = Survey
    template_name = 'survey_edit.html'
    form_class = SurveyModelForm
    # fields = ['title', 'faculty', 'description', 'start_date']
    # No se podra editar categoria porque de esto depende si los usuarios se pueden repetir por encuesta

    # def get(self, *args, **kwargs):
    #     survey_form = SurveyModelForm()
    #     formset = SurveyCareerFormSet(queryset=SurveyCareer.objects.none())
    #
    #     return self.render_to_response({'survey_form': survey_form, 'survey_career_form_set': formset})
    #
    # def post(self, *args, **kwargs):
    #     survey_form = SurveyModelForm(self.request.POST or None, self.request.FILES or None)
    #     formset = SurveyCareerFormSet(data=self.request.POST)
    #
    #     if survey_form.is_valid():
    #         survey_id = survey_form.save().pk
    #         if formset.is_valid():
    #             survey_career = formset.save(commit=False)
    #             for form in survey_career:
    #                 form.survey_id = survey_id
    #                 form.save()
    #
    #         return redirect(reverse_lazy("survey_edit", survey_id))
    #
    #     return self.render_to_response({'survey_form': survey_form, 'survey_career_form_set': formset})


class SurveyDelete(DeleteView):
    model = Survey
    success_url = reverse_lazy('surveys_index')


class DashboardAddView(CreateView):
    template_name = 'create_dashboard.html'
    form_class = DashboardForm
    success_url = 'dashboard_detail'


class DashboardAdminIndexView(ListView):
    model = Dashboard
    template_name = 'dashboard_admin_index.html'


class DashboardIndexView(ListView):
    model = Dashboard
    template_name = 'dashboard_index.html'


class DashboardDeleteView(DeleteView):
    model = Dashboard
    success_url = reverse_lazy('dashboard_index')


class DashboardDetailView(DetailView):
    model = Dashboard
    template_name = 'dashboard_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['dashboard_queries'] = DashboardQuery.objects.filter(dashboard=self.object.id)

        return context


class QueryAddView(CreateView):
    template_name = 'create_query2.html'

    # def form_valid(self, form):
    #     obj_dashboard = Dashboard.objects.get(pk=self.kwargs['pk'])
    #     obj_dashboard_query = DashboardQuery(dashboard=obj_dashboard, query=self.object)
    #     return super(QueryAddView,self).form_valid(form)
    #     # return reverse_lazy('home', kwargs={'pk': self.kwargs['pk']})

    def get_success_url(self):
        return reverse_lazy('dashboard_detail', kwargs={'pk': self.kwargs['pk']})

    def get(self, *args, **kwargs):
        query_form = QueryForm
        query_survey_question_form = QuerySurveyQuestionForm

        return self.render_to_response({'query_form': query_form,
                                        'query_survey_question_form': query_survey_question_form})

    def post(self, *args, **kwargs):
        query_form = QueryForm(self.request.POST or None)
        query_survey_question_form = QuerySurveyQuestionForm(self.request.POST or None)

        print(query_survey_question_form, query_form.is_valid())

        if query_form.is_valid() and query_survey_question_form.is_valid():
            obj_dashboard = Dashboard.objects.get(pk=self.kwargs['pk'])
            obj_query = query_form.save()
            obj_dashboard_query = DashboardQuery(dashboard=obj_dashboard, query=obj_query)
            obj_dashboard_query.save()
            query_survey_question_form.save(query_id=obj_query.pk)

        return self.render_to_response({'query_form': query_form,
                                        'query_survey_question_form': query_survey_question_form})


class DashboardView(TemplateView):
    template_name = "dashboard_Template.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['dashboard'] = Dashboard.objects.get(id=self.kwargs['pk'])
        context['dashboard_queries'] = DashboardQuery.objects.filter(dashboard=self.kwargs['pk'])

        tables = {}

        for dashboard_query in context['dashboard_queries']:
            if dashboard_query.query.graph_type == 'Table':
                answers = []
                obj_query_survey_question = QuerySurveyQuestion.objects.get(query=dashboard_query.query)
                objs_survey_question_answers = SurveyQuestionAnswer.objects.filter(
                    survey_question=obj_query_survey_question.survey_question)

                for obj_survey_question_answers in objs_survey_question_answers:
                    if obj_survey_question_answers.offered_answer.option_text != 'nan':

                        objs_answer = Answer.objects.filter(survey_question_answer=obj_survey_question_answers)
                        for obj in objs_answer:
                            if obj.answer_text != 'nan':
                                answers.append(obj)
                tables[dashboard_query.query.name] = answers

        context['table_answers'] = tables
        print(tables)

        return context


class ChartData(APIView):
    authentication_classes = []
    permission_classes = []

    def get(self, request, **kwargs):
        labels = []
        values = []
        question = []

        obj_query_survey_question = QuerySurveyQuestion.objects.get(query=self.kwargs['pk'])
        objs_survey_question_answers = SurveyQuestionAnswer.objects.filter(
            survey_question=obj_query_survey_question.survey_question)
        question.append(obj_query_survey_question.survey_question.question.question_text)

        # Get The labels
        for question_answers in objs_survey_question_answers:
            option = question_answers.offered_answer.option_text
            labels.append(option)

        # Get The values
        for question_answers in objs_survey_question_answers:
            n_answers = Answer.objects.filter(survey_question_answer=question_answers).count()
            values.append(n_answers)

        # Get rid of nan values
        if obj_query_survey_question.query.include_nan and 'nan' in labels:
            del values[labels.index('nan')]
            labels.remove('nan')
        elif 'nan' in labels:
            labels[labels.index('nan')] = 'Nulo'

        # Change to %
        if obj_query_survey_question.query.percentage_values:
            values = [round(x*100 / sum(values),2) for x in values]

        data = {
            "labels": labels,
            "values": values,
            "question": question,
        }
        return Response(data)


class FacultyAdminIndexView(ListView):
    model = Faculty
    template_name = 'facultys_admin_index.html'


class FacultyDetailView(DetailView):
    model = Faculty
    template_name = 'faculty_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['faculty_careers'] = Career.objects.filter(faculty=self.object.id)

        return context
