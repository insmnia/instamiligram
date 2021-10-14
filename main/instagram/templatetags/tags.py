from django import template
register = template.Library()

@register.simple_tag
def have_liked(post,user,*args,**kwargs):
    return post.likes.filter(id=user.id).exists()