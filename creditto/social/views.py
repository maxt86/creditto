from django.shortcuts import render
from django.views import View

from .models import Post

from .forms import PostForm
from .forms import CommentForm


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


class PostDetailView(View):
    
    def get(self, request, pk, *args, **kwargs):
        post = Post.objects.get(pk=pk)
        
        form = CommentForm()
        
        context = {
            'post': post,
            'form': form,
        }
        return render(request, 'social/post_detail.html', context)
    
    def post(self, request, *args, **kwargs):
        pass
