from django import template

register = template.Library()


@register.filter(name='max_size')
def max_size(width, width_max):
    return int(width_max) if int(width) > int(width_max) else int(width)
