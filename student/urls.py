from django.contrib.auth.decorators import login_required
from django.urls import path
from student.views import ResultDetailView, ResultListView, AssignmentDetailView, AssignmentListView, StudentHomePage, \
    USerUpdateView, change_password

app_name = 'student'

urlpatterns = [
    path('', login_required(StudentHomePage.as_view()), name='index'),
    path('result/', ResultListView.as_view(), name='results'),
    path('result/detail/<int:pk>/', ResultDetailView.as_view(), name='result-detail'),
    path('assignment/', AssignmentListView.as_view(), name='assigns'),
    path('assign/<int:pk>/', AssignmentDetailView.as_view(), name='assign-detail'),
    path('student/update/info/<int:pk>/', USerUpdateView.as_view(), name='student-user-update'),
    path('password/', change_password, name='change_password'),
]
