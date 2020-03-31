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

    if 101 > num >= 90.0:
        return 'A'
    elif 90 > num >= 80.0:
        return 'B+'
    elif 80 > num >= 70.0:
        return 'B'
    elif 70 > num >= 60.0:
        return 'C+'
    elif 60 > num >= 50.0:
        return 'C'
    elif 50 > num >= 40.0:
        return 'D'
    elif 40 > num >= 30.0:
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

    if 101 > num >= 90:
        return 'Excellent'
    elif 90 > num >= 80:
        return 'Very Good'
    elif 80 > num >= 70:
        return 'Good'
    elif 70 > num >= 60:
        return 'Fairly Satisfactory'
    elif 60 > num >= 50:
        return 'Satisfactory'
    elif 50 > num >= 40:
        return 'More Effort Required'
    elif 40 > num >= 30:
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

@register.filter(name='setting_repeat')
@stringfilter
def setting_repeat(value):
    """
    this grade student subjects
    :param value:
    :param arg:
    :return:
    """
    return set(value)

