from django import template
from django.template.defaultfilters import stringfilter
import json

register = template.Library()


@register.filter
@stringfilter
def to_json(string):
    string = string.replace('\'', '"')
    return json.loads(string)


@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)


@register.filter
def has_item(dictionary, key):
    if dictionary.get(key):
        return True
    else:
        return False


@register.filter
def get_answer(dictionary, key):
    key = "answer_" + str(key)
    return dictionary.get(key)


@register.filter
def color_slider(cycle, val):
    if cycle == 0 and val == 0:
        return "color"
    if cycle == 1 and val == 17:
        return "color"
    if cycle == 2 and val == 33:
        return "color"
    if cycle == 3 and val == 50:
        return "color"
    if cycle == 4 and val == 67:
        return "color"
    if cycle == 5 and val == 83:
        return "color"
    if cycle == 6 and val == 100:
        return "color"
    return ""


@register.filter
def color_standard(cycle, val):
    if cycle == 0 and val == 0:
        return "color"
    if cycle == 1 and val == 25:
        return "color"
    if cycle == 2 and val == 75:
        return "color"
    if cycle == 3 and val == 100:
        return "color"
    return ""


@register.filter
def color_budget(cycle, val):
    if cycle == 0 and val == 0:
        return "color"
    if cycle == 1 and val == 25:
        return "color"
    if cycle == 2 and val == 50:
        return "color"
    if cycle == 3 and val == 75:
        return "color"
    if cycle == 4 and val == 100:
        return "color"
    return ""
