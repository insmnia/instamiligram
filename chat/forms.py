from django import forms
from .models import Message


class SendMessageForm(forms.ModelForm):

    text = forms.CharField(widget=forms.TextInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'Write your message',
            'rows': 2,
            'columns': 30,
            'type': 'text',
            'id': 'send-msg',
        }
    ))

    class Meta:
        model = Message
        fields = ['text']
