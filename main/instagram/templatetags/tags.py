from django import template
from ..models import Post
register = template.Library()


@register.simple_tag
def have_liked(post, user, *args, **kwargs):
    return post.likes.filter(id=user.id).exists()


@register.simple_tag
def get_post_comments(post, *args, **kwargs):
    if len(post.comments.all()) >= 1:
        return post.comments.all()[len(post.comments.all())-1:]
    return []

@register.simple_tag
def have_saved(post,user,*args,**kwargs):
    return post.profiles.filter(id=user.id).exists()