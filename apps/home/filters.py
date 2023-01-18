# products/filters.py
from decimal import Decimal
from django.db.models import Q
import django_filters
from django.db.models import *
from django import template
from django.template.defaultfilters import stringfilter



register = template.Library()
@register.filter(name='split')
@stringfilter
def split(value, key):
    """
        Returns the value turned into a list.
    """
    return value.split(key)