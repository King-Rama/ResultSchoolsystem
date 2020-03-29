from django import template
from django.template.defaultfilters import stringfilter

register = template.Library()


@register.filter(name='grade_student')
@stringfilter
def grade_student(value):
    """
    this grade student subjects
    :param value:
    :param arg:
    :return:
    """
    grade = ''
    num = float(value)

    if 100 >= num >= 90:
        return 'A'
    elif 89 >= num >= 80:
        return 'B+'
    elif 79 >= num >= 70:
        return 'B'
    elif 69 >= num >= 60:
        return 'C+'
    elif 59 >= num >= 50:
        return 'C'
    elif 49 >= num >= 40:
        return 'D'
    elif 39 >= num >= 30:
        return 'E'
    elif num < 30:
        return 'F'


@register.filter(name='grade')
@stringfilter
def grade_student(value):
    """
    this grade student subjects
    :param value:
    :param arg:
    :return:
    """
    grade = ''
    num = float(value)

    if 100 >= num >= 90:
        return 'Excellent'
    elif 89 >= num >= 80:
        return 'Very Good'
    elif 79 >= num >= 70:
        return 'Good'
    elif 69 >= num >= 60:
        return 'Fairly Satisfactory'
    elif 59 >= num >= 50:
        return 'Satisfactory'
    elif 49 >= num >= 40:
        return 'More Effort Required'
    elif 39 >= num >= 30:
        return 'Below Required Standard'
    elif num < 30:
        return 'Fail'


@register.filter(name='round')
@stringfilter
def grade_student(value):
    """
    this grade student subjects
    :param value:
    :param arg:
    :return:
    """
    grade = ''
    num = float(value)
    return round(num, 1)
