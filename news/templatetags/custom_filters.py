from django import template


register = template.Library()


WORDS = ['редиска', 'баран', 'скотина']


@register.filter()
def censor(value):
    for i in value.split():
        if i in WORDS:
            value = value.replace(i, "*" * len(i))
    return f'{value}'
