from django import template
register = template.Library()


@register.simple_tag
def crop_msg(msg: str, *args, **kwargs):
    if len(msg) > 255:
        msg = msg[:255]+'...'
    return msg
