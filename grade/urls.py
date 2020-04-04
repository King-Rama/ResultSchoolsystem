from django.contrib.auth.decorators import login_required
from django.urls import path
from .views import AssignCreateView, AssignUpdateView, AssignDetailView, AssignDeleteView, AssignListView, \
    StudentListView, GradeHomePage, StudentDetailView, ResultListView, ResultDetailView, upload_result_master, \
    change_password, upload_result, ResultCaseListView, ResultCaseDeleteView, ResultCaseDetailView, DeleteAllStudents, delete_all, reset_password

app_name = 'grade'

urlpatterns = [
    path('upload/', upload_result_master, name='master-doc'),
    path('', login_required(GradeHomePage.as_view()), name='index'),
    path('new-assignment/', AssignCreateView.as_view(), name='assign'),
    path('list-assignment/', AssignListView.as_view(), name='assign-list'),
    path('update-assignment/<int:pk>/', AssignUpdateView.as_view(), name='assign-update'),
    path('detail-assignment/<int:pk>/', AssignDetailView.as_view(), name='assign-detail'),
    path('delete-assignment/<int:pk>/', AssignDeleteView.as_view(), name='assign-delete'),
    path('student/', StudentListView.as_view(), name='students'),
    path('student-detail/<int:pk>/', StudentDetailView.as_view(), name='student-detail'),
    path('result/', upload_result, name='normal-result'),
    path('result/list/', ResultListView.as_view(), name='result-list'),
    path('result/detail/<int:pk>/', ResultDetailView.as_view(), name='result-detail'),
    path('password/', change_password, name='change_password'),
    path('result/list/cases/', ResultCaseListView.as_view(), name='results-case'),
    path('result/detail/cases/<int:pk>/', ResultCaseDetailView.as_view(), name='result-case-detail'),
    path('result/delete/cases/<int:pk>/', ResultCaseDeleteView.as_view(), name='result-case-delete'),
    path('school-end/delete/all/', DeleteAllStudents.as_view(), name='desolve-all'),
    path('school-end/delete/confirmed/', delete_all, name='desolve-all-confirm'),
    path('pass/reset/student/', reset_password, name='reset-pass'),

]
