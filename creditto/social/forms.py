from django import forms

from .models import Post
from .models import Comment
from .models import Message


class PostForm(forms.ModelForm):
    
    content = forms.CharField(
        label='',
        widget=forms.Textarea(attrs={
            'rows': 2,
            'placeholder': 'Tell the world something...',
        }),
    )
    
    image = forms.ImageField(
        label='',
        required=False,
        widget=forms.ClearableFileInput(attrs={
            'multiple': True,
        }),
    )
    
    class Meta:
        model = Post
        fields = ['content']


class CommentForm(forms.ModelForm):
    
    comment = forms.CharField(
        label='',
        widget=forms.Textarea(attrs={
            'rows': 1,
            'style': 'resize: none; overflow: hidden',
        }),
    )
    
    class Meta:
        model = Comment
        fields = ['comment']


class ThreadForm(forms.Form):
    username = forms.CharField(label='', max_length=100)


class MessageForm(forms.ModelForm):
    
    content = forms.CharField(label='', max_length=1000)
    
    image = forms.ImageField(label='', required=False)
    
    class Meta:
        model = Message
        fields = ['content', 'image']


class ShareForm(forms.Form):
    content = forms.CharField(
        label='',
        widget=forms.Textarea(attrs={
            'rows': '1',
            'style': 'resize: none; overflow: hidden',
            'placeholder': 'Say something...',
        }),
    )
