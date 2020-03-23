import pandas as pd
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.db import IntegrityError
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import TemplateView, CreateView, ListView, UpdateView, DeleteView, DetailView
# Create your views here.
from xlrd import XLRDError

from .models import Results, Student, Grade, User, Assignment
from .forms import DocUploadForm, AssignmentCreateForm
from .decorators import teacher_required, teacher_and_staff_required
from django.utils.decorators import method_decorator
from django.contrib import messages

#
# @method_decorator([login_required, teacher_and_staff_required], name='dispatch')
# class UploadGradeView(CreateView):
#     template_name = 'grade/result-upload/master_doc.html'
#     context_object_name = 'form'
#     form_class = DocUploadForm
#     success_url = reverse_lazy('grade:index')
#
#     def form_valid(self, form):
#         file = form.cleaned_data['file']
#         if file.name.endswith('.xls'):
#             pass
#         else:
#             messages.add_message(self.request, messages.INFO, 'File is not an excel / spreadsheet file.')
#             return self.form_invalid(form)
#         count = 0
#         try:
#
#             # data entry starts here
#             book = pd.read_excel(file).fillna(value='-')
#
#             for student in range(len(book)):
#                 header = list(book.iloc[student])
#                 first_name, middle_name, last_name = header[0].split(' ')[0], header[0].split(' ')[-2], \
#                                                      header[0].split(' ')[-1]
#                 username = str('{}_{}'.format(first_name, last_name)).lower()
#                 password = str(last_name.upper())
#                 level, stream, of, year = header[1].split(' ')
#                 room = '{}{}{}{}'.format(level, stream, of, year).lower()
#                 # register classroom user
#                 if count < 1:
#                     grade_room = User.objects.create(username=room, password='burhani', is_teacher=True)
#                     grade_room.set_password('burhani')
#                     grade_room.save()
#                     # then add classroom FK
#                     roomy = Grade(room=grade_room, year=year, level=level, stream=stream)
#                     roomy.save()
#                     count = 2
#                 # register student user
#                 st = User.objects.create(username=username, middle_name=middle_name, first_name=first_name,
#                                          last_name=last_name, is_student=True)
#                 st.set_password(password)
#                 st.save()
#                 # creating new students
#                 stu = Student(user=st, class_room=roomy)
#                 stu.save()
#
#                 # creating new results
#                 new_results = Results(user=stu, exam_name=header[2], maths=header[3],
#                                       english=header[4], health=header[5], kusoma=header[6], arts_sports=header[7],
#                                       kiswahili=header[8], science_tech=header[9], civics_moral=header[10],
#                                       social_studies=header[11], geography=header[12], history=header[13], ict=header[14],
#                                       v_skills=header[15], pds=header[16], science=header[17], subject_taken=header[18],
#                                       marks=header[19], mean_score=header[20])
#
#                 new_results.save()
#
#         except IntegrityError as error:
#
#
#         return self.form_valid(form)

@login_required
@teacher_and_staff_required
def upload_result_master(request):
    form = DocUploadForm(request.POST, request.FILES)
    count = 0
    # files = request.FILES['file'].name
    # print(files)
    # if request.FILES.get('file', False):
    #     pass
    # else:
    #     messages.add_message(request, messages.ERROR, 'Urecognized file type')
    #     redirect('grade:master-doc')

    if form.is_valid():
        try:
            book = pd.read_excel(request.FILES['file']).fillna(value='-')
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
                    grade_room = User.objects.create(username=room, password='burhani', is_teacher=True)
                    grade_room.set_password('burhani')
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
            messages.add_message(request, messages.ERROR, 'Document added successfully and class: {} created '.format(grade_room.username))
            redirect('grade:master-doc')

        except XLRDError as erro1:
            messages.add_message(request, messages.ERROR, 'Unrecognized document, please upload an excel file')
            redirect('grade:master-doc')

        except IntegrityError as error:
            messages.add_message(request, messages.ERROR, 'Document already added!')
            redirect('grade:master-doc')

    return render(request, 'grade/result-upload/master_doc.html', {'form': form})


@method_decorator([login_required, teacher_required], name='dispatch')
class StudentListView(ListView):
    template_name = 'grade/student/list.html'
    model = Student
    context_object_name = 'students'

    def get_queryset(self):
        return Student.objects.filter(class_room__room=self.request.user).order_by('user__first_name')


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


@method_decorator([login_required, teacher_and_staff_required], name='dispatch')
class GradeHomePage(TemplateView):
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
    fields = ['title', 'description', 'file']
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
class AssignDeleteView(SuccessMessageMixin, DeleteView):
    model = Assignment
    template_name = 'grade/assign/confirm.html'
    context_object_name = 'assign_delete'
    success_url = reverse_lazy('grade:assign-list')
    success_message = 'Assignment/Announcement deleted successful'

    def form_valid(self, form):
        messages.add_message(self.request, messages.INFO, 'Assignment deleted successfully')
        return super(AssignListView)

#
# @method_decorator([login_required, teacher_required], name='dispatch')
# class UploadNormalResultView(SuccessMessageMixin, CreateView):
#     template_name = 'grade/result-upload/master_doc.html'
#     context_object_name = 'form'
#     form_class = DocUploadForm
#     success_url = reverse_lazy('grade:index')
#     success_message = "Results uploaded successfully"
#
#     def form_valid(self, form):
#         file = form.cleaned_data['file']
#         count = 0
#         try:
#             # data entry starts here
#             book = pd.read_excel(file).fillna(value='-')
#
#             for student in range(len(book)):
#                 header = list(book.iloc[student])
#                 first_name, middle_name, last_name = header[0].split(' ')[0], header[0].split(' ')[-2], \
#                                                      header[0].split(' ')[-1]
#                 username = str('{}_{}'.format(first_name, last_name)).lower()
#                 password = str(last_name.upper())
#                 level, stream, of, year = header[1].split(' ')
#                 room = '{}{}{}{}'.format(level, stream, of, year).lower()
#                 # register classroom user
#
#                 # register student user
#                 st = User.objects.get(username=username)
#                 # creating new students
#                 stu = Student.objects.get(st.id)
#
#                 # creating new results
#                 new_results = Results(user=stu, exam_name=header[2], maths=header[3],
#                                       english=header[4], health=header[5], kusoma=header[6], arts_sports=header[7],
#                                       kiswahili=header[8], science_tech=header[9], civics_moral=header[10],
#                                       social_studies=header[11], geography=header[12], history=header[13],
#                                       ict=header[14],
#                                       v_skills=header[15], pds=header[16], science=header[17], subject_taken=header[18],
#                                       marks=header[19], mean_score=header[20])
#
#                 new_results.save()
#             return super().form_valid(form)
#
#         except IntegrityError as error:
#             return reverse_lazy('grade:index')


@login_required
@teacher_and_staff_required
def upload_result(request):
    form = DocUploadForm(request.POST, request.FILES)
    count = 0
    # files = request.FILES['file'].name
    # print(files)
    # if request.FILES.get('file', False):
    #     pass
    # else:
    #     messages.add_message(request, messages.ERROR, 'Urecognized file type')
    #     redirect('grade:master-doc')

    if form.is_valid():
        try:
            book = pd.read_excel(request.FILES['file']).fillna(value='-')
            header = list(book.iloc[0])
            if Results.objects.filter(exam_name=header[2]).count() > 0:
                raise ImportError

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

                    grade_room = User.objects.get(username=request.user.username)

                    # then add classroom FK
                    roomy = Grade.objects.get(room=grade_room, year=year, level=level, stream=stream)
                    count = 2
                # register student user
                st = User.objects.get(username=username)
                # creating new students
                stu = Student.objects.get(user=st, class_room=roomy)


                # creating new results
                new_results = Results(user=stu, exam_name=header[2], maths=header[3],
                                      english=header[4], health=header[5], kusoma=header[6], arts_sports=header[7],
                                      kiswahili=header[8], science_tech=header[9], civics_moral=header[10],
                                      social_studies=header[11], geography=header[12], history=header[13], ict=header[14],
                                      v_skills=header[15], pds=header[16], science=header[17], subject_taken=header[18],
                                      marks=header[19], mean_score=header[20])

                new_results.save()
            messages.add_message(request, messages.ERROR, 'Document added successfully and class: {} have one new results '.format(grade_room.username))
            redirect('grade:normal-result')

        except XLRDError as erro1:
            messages.add_message(request, messages.ERROR, 'Unrecognized document, please upload an excel file')
            redirect('grade:normal-result')

        except IntegrityError as error:
            messages.add_message(request, messages.ERROR, 'Document already added!')
            redirect('grade:normal-result')

        except ImportError as error:
            messages.add_message(request, messages.ERROR, '{} is already added, please add a new result document'.format(header[2]))
            redirect('grade:normal-result')

    return render(request, 'grade/result-upload/master_doc.html', {'form': form})






@method_decorator([login_required, teacher_required], name='dispatch')
class GradeDetailView(DetailView):
    model = Grade
    template_name = 'grade/room/detail.html'
    context_object_name = 'grade_detail'


@method_decorator([login_required, teacher_and_staff_required], name='dispatch')
class UserUpdateView(UpdateView):
    model = User

    fields = ['username',]
    template_name = 'grade/update.html'
    context_object_name = 'st_user'

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context['stu'] = Student.class_room
    #     return context


@login_required
@teacher_and_staff_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Your password was successfully updated!')
            return redirect('student:index')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'grade/room/change_password.html', {
        'form': form
    })