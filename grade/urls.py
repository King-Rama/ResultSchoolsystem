from django.urls import path
from .views import AssignCreateView, AssignUpdateView, AssignDetailView, AssignDeleteView, AssignListView, \
    StudentListView, GradeHomePage, UploadGradeView, UploadNormalResultView, StudentDetailView, ResultListView, ResultDetailView

app_name = 'grade'

urlpatterns = [
    path('upload/', UploadGradeView.as_view(), name='master-doc'),
    path('', GradeHomePage.as_view(), name='index'),
    path('new-assignment/', AssignCreateView.as_view(), name='assign'),
    path('list-assignment/', AssignListView.as_view(), name='assign-list'),
    path('update-assignment/<int:pk>/', AssignUpdateView.as_view(), name='assign-update'),
    path('detail-assignment/<int:pk>/', AssignDetailView.as_view(), name='assign-detail'),
    path('delete-assignment/<int:pk>/', AssignDeleteView.as_view(), name='assign-delete'),
    path('student/', StudentListView.as_view(), name='students'),
    path('student-detail/<int:pk>/', StudentDetailView.as_view(), name='student-detail'),
    path('result/', UploadNormalResultView.as_view(), name='normal-result'),
    path('result/list/', ResultListView.as_view(), name='result-list'),
    path('result/detail/<int:pk>/', ResultDetailView.as_view(), name='result-detail'),

]