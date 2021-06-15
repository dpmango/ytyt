from functools import wraps

from django import template

register = template.Library()


def force_int(func):

    @wraps(func)
    def wrapper(*args):
        func(*[int(arg) for arg in args])

    return wrapper


@register.filter(name='max_size')
@force_int
def max_size(width, width_max):
    return width_max if width > width_max else width
