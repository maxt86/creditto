from django import forms

from .models import Post
from .models import Comment


class PostForm(forms.ModelForm):
    
    content = forms.CharField(
        label='',
        widget=forms.Textarea(attrs={
            'rows': 2,
            'placeholder': 'Tell the world something...',
        })
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
        })
    )
    
    class Meta:
        model = Comment
        fields = ['comment']
