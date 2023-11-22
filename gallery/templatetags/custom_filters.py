from django import template

register = template.Library()


@register.filter(name='wordcount')
def wordcount(value, count):
    words = value.split()
    return ' '.join(words[:count])
