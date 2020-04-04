from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect

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
