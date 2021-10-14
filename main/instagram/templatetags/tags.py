from django import template
from ..models import Post
register = template.Library()

@register.simple_tag
def have_liked(post,user,*args,**kwargs):
    return post.likes.filter(id=user.id).exists()

@register.simple_tag
def get_post_comments(post,*args,**kwargs):
    return post.comments.all()[len(post.comments.all())-2:]