from django import template
from ..models import Post,Like
from django.contrib.contenttypes.models import ContentType

register = template.Library()


@register.simple_tag
def have_liked(post, user, *args, **kwargs):
    like_obj = Like.objects.filter(
            content_type=ContentType.objects.get_for_model(post), object_id=post.id, user=user
        )
    return like_obj.exists()

@register.simple_tag
def have_liked_comment(comment, user, *args, **kwargs):
    like_obj = Like.objects.filter(
            content_type=ContentType.objects.get_for_model(comment), object_id=comment.id, user=user
        )
    return like_obj

@register.simple_tag
def get_post_comments(post, *args, **kwargs):
    if len(post.comments.all()) >= 2:
        return post.comments.all()[len(post.comments.all())-2:]
    if len(post.comments.all()) == 1:
        return post.comments.all()[len(post.comments.all())-1:]
    return []

@register.simple_tag
def have_saved(post,user,*args,**kwargs):
    return post.profiles.filter(id=user.id).exists()