from django import forms
from .models import Message


class SendMessageForm(forms.ModelForm):

    text = forms.CharField(widget=forms.Textarea(
        attrs={
            'class': 'form-control',
            'placeholder': 'Write your message',
            'rows': 2,
            'columns': 30,
            'type': 'submit',
            'id': 'send-msg'
        }
    ))

    class Meta:
        model = Message
        fields = ['text']
