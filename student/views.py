from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import request
from django.shortcuts import render, redirect
from django.views import generic

from chartjs.views.lines import BaseLineChartView

# Create your views here.
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView, ListView, DetailView, UpdateView

from grade.decorators import student_required
from grade.models import Results, Assignment, User, Student



@method_decorator([student_required], name='dispatch')
class StudentHomePage(TemplateView):
    template_name = 'student/base.html'


@method_decorator([login_required, student_required], name='dispatch')
class ResultListView(ListView):
    model = Results
    template_name = 'student/result/list.html'
    context_object_name = 'results'

    def get_queryset(self):
        return Results.objects.filter(user__user__username=self.request.user)


@method_decorator([login_required, student_required], name='dispatch')
class ResultDetailView(DetailView):
    model = Results
    template_name = 'student/result/detail.html'
    context_object_name = 'result_detail'


@method_decorator([login_required, student_required], name='dispatch')
class AssignmentListView(ListView):
    model = Assignment
    template_name = 'student/assign/list.html'
    context_object_name = 'assignments'

    def get_queryset(self):
        return Assignment.objects.filter(uploader__grade_member__user=self.request.user)


@method_decorator([login_required, student_required], name='dispatch')
class AssignmentDetailView(DetailView):
    model = Assignment
    template_name = 'student/assign/detail.html'
    context_object_name = 'assign_detail'


@method_decorator([login_required, student_required], name='dispatch')
class USerUpdateView(DetailView):
    model = User
    template_name = 'student/update.html'
    context_object_name = 'st_user'

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context['stu'] = Student.class_room
    #     return context


@login_required
@student_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.add_message(request, messages.SUCCESS, 'Your password was successfully updated!')
            return redirect('student:index')
        else:
            messages.add_message(request, messages.ERROR, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'accounts/change_password.html', {
        'form': form
    })


class LineChartJSONView(BaseLineChartView):
    model = Results

    def get_labels(self):
        """labesls"""
        subjects = []
        qs = Results.objects.filter(user__user=self.request.user)[0]
        if qs.maths != str('-'):
            subjects.append('Mathemaics')

        if qs.english != str('-'):
            subjects.append('English')

        if qs.health != str('-'):
            subjects.append('Health')

        if qs.kusoma != str('-'):
            subjects.append('Kusoma')

        if qs.arts_sports != str('-'):
            subjects.append('Arts and Sports')

        if qs.kiswahili != str('-'):
            subjects.append('Kiswahili')

        if qs.science_tech != str('-'):
            subjects.append('Science Tech')

        if qs.civics_moral != str('-'):
            subjects.append('Civics Moral')

        if qs.social_studies != str('-'):
            subjects.append('Social Studies')

        if qs.geography != str('-'):
            subjects.append('Geography')

        if qs.history != str('-'):
            subjects.append('History')

        if qs.ict != str('-'):
            subjects.append('ICT')

        if qs.v_skills != str('-'):
            subjects.append('Vocational Skills')

        if qs.pds != str('-'):
            subjects.append('PDS')

        if qs.science != str('-'):
            subjects.append('Science')
        return subjects

    def get_providers(self):
        """names of data-sets"""
        exams = []
        res = Results.objects.filter(user__user=self.request.user)
        for qs in res:
            exams.append(qs.exam_name.exam_name_cl)
        exam_recorded = []
        for exam in exams:
            take = str(exam.split('-')[1]+'-'+exam.split('-')[-1])
            exam_recorded.append(take)
        return exam_recorded



    def get_data(self):
        """datasets to be plotted"""

        res = Results.objects.filter(user__user=self.request.user)
        subjects = [[] for x in range(len(res))]
        num = 0
        for qs in res:
            subjects[num] = []
            if qs.maths != str('-'):
                subjects[num].append(int(qs.maths))

            if qs.english != str('-'):
                subjects[num].append(int(qs.english))

            if qs.health != str('-'):
                subjects[num].append(int(qs.health))

            if qs.kusoma != str('-'):
                subjects[num].append(int(qs.kusoma))

            if qs.arts_sports != str('-'):
                subjects[num].append(int(qs.arts_sports))

            if qs.kiswahili != str('-'):
                subjects[num].append(int(qs.kiswahili))

            if qs.science_tech != str('-'):
                subjects[num].append(int(qs.science_tech))

            if qs.civics_moral != str('-'):
                subjects[num].append(int(qs.civics_moral))

            if qs.social_studies != str('-'):
                subjects[num].append(int(qs.social_studies))

            if qs.geography != str('-'):
                subjects[num].append(int(qs.geography))

            if qs.history != str('-'):
                subjects[num].append(int(qs.history))

            if qs.ict != str('-'):
                subjects[num].append(int(qs.ict))

            if qs.v_skills != str('-'):
                subjects[num].append(int(qs.v_skills))

            if qs.pds != str('-'):
                subjects[num].append(int(qs.pds))

            if qs.science != str('-'):
                subjects[num].append(int(qs.science))
            num = num + 1
        return subjects


line_chart = TemplateView.as_view(template_name='student/result/detail.html')
line_chart_json = LineChartJSONView.as_view()


def result_chart(request):
    labels = []
    data = []

    queryset = Results.objects.values('')