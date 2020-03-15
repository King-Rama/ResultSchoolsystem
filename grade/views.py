import pandas as pd
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.mail import message
from django.db import IntegrityError
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import TemplateView, CreateView, ListView, UpdateView, DeleteView, DetailView
# Create your views here.
from .models import Results, Student, Grade, User, Assignment
from .forms import DocUploadForm, AssignmentCreateForm
from .decorators import student_required, teacher_required
from django.utils.decorators import method_decorator
from django.contrib import messages


class UploadGradeView(LoginRequiredMixin, CreateView):
    template_name = 'grade/result-upload/master_doc.html'
    context_object_name = 'form'
    form_class = DocUploadForm
    success_url = '/'

    def form_valid(self, form):
        file = form.cleaned_data['file']
        count = 0
        try:
            # data entry starts here
            book = pd.read_excel(file).fillna(value='NOT')

            for student in range(len(book)):
                header = list(book.iloc[student])
                first_name, middle_name, last_name = header[0].split(' ')[0], header[0].split(' ')[-2], \
                                                     header[0].split(' ')[-1]
                username = str('{}_{}'.format(first_name, last_name)).lower()
                password = str(last_name.upper())
                level, stream, of, year = header[1].split(' ')
                room = '{}{}{}{}'.format(level, stream, of, year).lower()
                # register classroom user
                if count < 1:
                    grade_room = User.objects.create(username=room, password='burhan', is_teacher=True)
                    grade_room.set_password('burhan')
                    grade_room.save()
                    # then add classroom FK
                    roomy = Grade(room=grade_room, year=year, level=level, stream=stream)
                    roomy.save()
                    count = 2
                # register student user
                st = User.objects.create(username=username, middle_name=middle_name, first_name=first_name,
                                         last_name=last_name, is_student=True)
                st.set_password(password)
                st.save()
                # creating new students
                stu = Student(user=st, class_room=roomy)
                stu.save()

                # creating new results
                new_results = Results(user=stu, exam_name=header[2], maths=header[3],
                                      english=header[4], health=header[5], kusoma=header[6], arts_sports=header[7],
                                      kiswahili=header[8], science_tech=header[9], civics_moral=header[10],
                                      social_studies=header[11], geography=header[12], history=header[13], ict=header[14],
                                      v_skills=header[15], pds=header[16], science=header[17], subject_taken=header[18],
                                      marks=header[19], mean_score=header[20])

                new_results.save()
            return super().form_invalid(form)

        except IntegrityError as error:
            messages.add_message(self.request, messages.INFO, 'File Already added!')
            return self.form_invalid(form)


@method_decorator([login_required, teacher_required], name='dispatch')
class StudentListView(ListView):
    template_name = 'grade/student/list.html'
    model = Student
    context_object_name = 'students'

    def get_queryset(self):
        return Student.objects.filter(class_room__room=self.request.user)


@method_decorator([login_required, teacher_required], name='dispatch')
class StudentDetailView(DetailView):
    template_name = 'grade/student/detail.html'
    model = Student
    context_object_name = 'student'


@method_decorator([login_required, teacher_required], name='dispatch')
class ResultListView(ListView):
    template_name = 'grade/result/list.html'
    model = Results
    context_object_name = 'results'


@method_decorator([login_required, teacher_required], name='dispatch')
class ResultDetailView(DetailView):
    template_name = 'grade/result/detail.html'
    model = Results
    context_object_name = 'result_detail'


@method_decorator([login_required, teacher_required], name='dispatch')
class ClassRoomListView(ListView):
    model = Grade


class GradeHomePage(LoginRequiredMixin, TemplateView):
    template_name = 'grade/base_grade.html'


@method_decorator([login_required, teacher_required], name='dispatch')
class AssignCreateView(CreateView):
    model = Assignment
    fields = ['title', 'description', 'file']
    template_name = 'grade/assign/create.html'
    context_object_name = 'assign_create'

    def form_valid(self, form):
        assign_create = form.save(commit=False)
        assign_create.uploader = Grade.objects.get(room__username=self.request.user)
        assign_create.save()
        return super().form_valid(form)


@method_decorator([login_required, teacher_required], name='dispatch')
class AssignUpdateView(UpdateView):
    model = Assignment
    fields = ['title', 'desc', 'file']
    template_name = 'grade/assign/update.html'
    context_object_name = 'assign_update'


@method_decorator([login_required, teacher_required], name='dispatch')
class AssignListView(ListView):
    model = Assignment
    paginate_by = 10
    template_name = 'grade/assign/list.html'
    context_object_name = 'assign_list'

    def get_queryset(self):
        return Assignment.objects.filter(uploader__room__username=self.request.user)


@method_decorator([login_required, teacher_required], name='dispatch')
class AssignDetailView(DetailView):
    model = Assignment
    template_name = 'grade/assign/detail.html'
    context_object_name = 'assign_detail'


@method_decorator([login_required, teacher_required], name='dispatch')
class AssignDeleteView(DeleteView):
    model = Assignment
    template_name = 'grade/assign/confirm.html'
    context_object_name = 'assign_delete'
    success_url = reverse_lazy('grade:assign-list')


@method_decorator([login_required, teacher_required], name='dispatch')
class UploadNormalResultView(CreateView):
    template_name = 'grade/result-upload/master_doc.html'
    context_object_name = 'form'
    form_class = DocUploadForm
    success_url = reverse_lazy('grade:index')

    def form_valid(self, form):
        file = form.cleaned_data['file']
        count = 0
        try:
            # data entry starts here
            book = pd.read_excel(file).fillna(value='NOT')

            for student in range(len(book)):
                header = list(book.iloc[student])
                first_name, middle_name, last_name = header[0].split(' ')[0], header[0].split(' ')[-2], \
                                                     header[0].split(' ')[-1]
                username = str('{}_{}'.format(first_name, last_name)).lower()
                password = str(last_name.upper())
                level, stream, of, year = header[1].split(' ')
                room = '{}{}{}{}'.format(level, stream, of, year).lower()
                # register classroom user

                # register student user
                st = User.objects.get(username=username)
                # creating new students
                stu = Student.objects.get(st.id)

                # creating new results
                new_results = Results(user=stu, exam_name=header[2], maths=header[3],
                                      english=header[4], health=header[5], kusoma=header[6], arts_sports=header[7],
                                      kiswahili=header[8], science_tech=header[9], civics_moral=header[10],
                                      social_studies=header[11], geography=header[12], history=header[13],
                                      ict=header[14],
                                      v_skills=header[15], pds=header[16], science=header[17], subject_taken=header[18],
                                      marks=header[19], mean_score=header[20])

                new_results.save()
            return super().form_valid(form)

        except IntegrityError as error:
            return reverse_lazy('grade:index')


@method_decorator([login_required, teacher_required], name='dispatch')
class GradeDetailView(DetailView):
    model = Grade
    template_name = 'grade/room/detail.html'
    context_object_name = 'grade_detail'
