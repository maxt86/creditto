from django import forms

from .models import Post


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
