from django import template
register = template.Library()

@register.simple_tag
def is_following(user,target_user,*args,**kwargs):
    return target_user.profile.followers.filter(id=user.id).exists()