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
    num = int(value)

    if 100 >= num >= 80:
        return 'A'
    elif 80 >= num >= 61:
        return 'B'
    elif 60 >= num >= 41:
        return 'C'
    elif num <= 40:
        return 'D'


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
    num = int(value)

    if 100 >= num >= 80:
        return 'Excellent'
    elif 80 >= num >= 61:
        return 'Good'
    elif 60 >= num >= 41:
        return 'Average'
    elif num <= 40:
        return 'Poor'


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
