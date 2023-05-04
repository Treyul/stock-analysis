from django import template

register = template.Library()


@register.simple_tag
def update_add_var(value):
    return value + 1


@register.simple_tag
def update_sub_var(value):
    return value - 1