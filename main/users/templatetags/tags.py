from django import template
from instagram.models import Post
register = template.Library()

@register.simple_tag
def is_following(user,target_user,*args,**kwargs):
    return target_user.profile.followers.filter(id=user.id).exists()

@register.simple_tag
def get_user_posts(user,*args,**kwargs):
    return Post.objects.filter(author=user).all()