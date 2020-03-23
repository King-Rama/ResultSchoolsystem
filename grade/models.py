from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse
from django.utils import timezone


# Create your models here.


class User(AbstractUser):

    is_student = models.BooleanField(default=False)
    is_teacher = models.BooleanField(default=False)
    middle_name = models.CharField(max_length=20, blank=True)


class Grade(models.Model):
    room = models.OneToOneField(User, on_delete=models.CASCADE, related_name='school_classrooms')
    year = models.PositiveSmallIntegerField()
    level = models.CharField(max_length=5, null=True)
    stream = models.CharField(max_length=5, null=True)

    def __str__(self):
        return self.stream

    def get_absolute_url(self):
        return reverse('grade:grade-detail', kwargs={'pk': self.id})


class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='students')
    class_room = models.ForeignKey('Grade', on_delete=models.CASCADE, related_name='grade_member')

    @property
    def fullname(self):
        f_name = self.user.first_name
        m_name = self.user.middle_name
        l_name = self.user.last_name
        return f_name + ' ' + m_name + ' ' + l_name

    def __str__(self):
        return self.fullname

    def get_absolute_url(self):
        return reverse('grade:student-detail', kwargs={'pk': self.id})


class ResultFileUpload(models.Model):
    exam_name = models.CharField(max_length=50)
    description = models.TextField()
    created = models.DateField(default=timezone.now)
    file = models.FileField(upload_to='result/excel/', null=True)

    def __str__(self):
        return self.exam_name


class Results(models.Model):
    user = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='student_result')
    exam_name = models.CharField(max_length=100)
    maths = models.CharField(null=True, max_length=4)
    english = models.CharField(null=True, max_length=4)
    health = models.CharField(null=True, max_length=4)
    kusoma = models.CharField(null=True, max_length=4)
    arts_sports = models.CharField(null=True, max_length=4)
    kiswahili = models.CharField(null=True, max_length=4)
    science_tech = models.CharField(null=True, max_length=4)
    civics_moral = models.CharField(null=True, max_length=4)
    social_studies = models.CharField(null=True, max_length=4)
    geography = models.CharField(null=True, max_length=4)
    history = models.CharField(null=True, max_length=4)
    ict = models.CharField(null=True, max_length=4)
    v_skills = models.CharField(null=True, max_length=4)
    pds = models.CharField(null=True, max_length=4)
    science = models.CharField(null=True, max_length=4)
    subject_taken = models.CharField(null=True, max_length=4)
    marks = models.CharField(null=True, max_length=4)
    mean_score = models.CharField(null=True, max_length=4)

    @property
    def fullname(self):
        f_name = self.user.user.first_name
        m_name = self.user.user.middle_name
        l_name = self.user.user.last_name
        return f_name+' '+m_name+' '+l_name

    def __str__(self):
        return self.fullname

    def get_absolute_url(self):
        return reverse('student:result-detail', kwargs={'pk': self.id})


class Assignment(models.Model):
    title = models.CharField(max_length=50)
    description = models.TextField()
    created = models.DateField(default=timezone.now)
    file = models.FileField(blank=True, null=True)
    uploader = models.ForeignKey(Grade, on_delete=models.CASCADE, related_name='file_uploader')

    def __str__(self):
        return self.title+' Created on'+str(self.created)

    def get_absolute_url(self):
        return reverse('grade:assign-detail', kwargs={'pk': self.id})

