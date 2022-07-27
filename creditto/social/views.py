from django.shortcuts import render
from django.views import View

from .models import Post
from .forms import PostForm


class PostsView(View):
    
    def get(self, request, *args, **kwargs):
        posts = Post.objects.all().order_by('-created')
        
        form = PostForm()
        
        context = {
            'posts': posts,
            'form': form,
        }
        return render(request, 'social/posts.html', context)
    
    def post(self, request, *args, **kwargs):
        posts = Post.objects.all().order_by('-created')
        
        form = PostForm(request.POST)
        if form.is_valid():
            new_post = form.save(commit=False)
            new_post.author = request.user
            new_post.save()
        
        context = {
            'posts': posts,
            'form': form,
        }
        return render(request, 'social/posts.html', context)
