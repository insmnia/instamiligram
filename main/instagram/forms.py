from django import forms
from .models import Comment, Post


class CreatePostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title','content','image','tags']
    
    def clean_tags(self):
        tags = self.cleaned_data['tags']
        return tags[0].split()

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']

    content = forms.CharField(widget=forms.Textarea(
        attrs={
            'class': 'form-control',
            'placeholder': 'Write your comment',
            'rows': 2,
            'columns': 30,
            'type': 'submit',
            'id': 'commentMsg'
        }
    ))
