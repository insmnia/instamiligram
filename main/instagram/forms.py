from django import forms
from .models import Comment, Post


class CreatePostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content', 'image', 'tags']

    title = forms.CharField(widget=forms.TextInput(
        attrs={
            'class': 'form-control',
            'id': 'title',
            'placeholder': 'Title'
        }
    ))

    content = forms.CharField(widget=forms.Textarea(
        attrs={
            'class': 'form-control',
            'id': 'content',
            'rows': 3,
            'placeholder': 'Your content here'
        }
    ))
    image = forms.FileField(widget=forms.FileInput(
        attrs={
            'class': 'form-control',
            'type': 'file',
            'id': 'image'
        }
    ))
    tags = forms.CharField(widget=forms.TextInput(
        attrs={
            'class': 'form-control',
            'id': 'tags',
            'placeholder': '#yourtaghere #anothertaghere'
        }
    ), required=False)

    def clean_tags(self):
        if self.cleaned_data['tags']:
            tags = self.cleaned_data['tags']
            return tags.split()
        return []


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
