from django.shortcuts import render
from django.urls import reverse_lazy

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.mixins import UserPassesTestMixin

from django.views import View
from django.views.generic.edit import UpdateView, DeleteView

from .models import Post
from .models import Comment

from .forms import PostForm
from .forms import CommentForm


class PostsView(LoginRequiredMixin, View):
    
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


class PostDetailView(LoginRequiredMixin, View):
    
    def get(self, request, pk, *args, **kwargs):
        post = Post.objects.get(pk=pk)
        
        form = CommentForm()
        
        comments = Comment.objects.filter(post=post).order_by('-created')
        
        context = {
            'post': post,
            'form': form,
            'comments': comments,
        }
        return render(request, 'social/post_detail.html', context)
    
    def post(self, request, pk, *args, **kwargs):
        post = Post.objects.get(pk=pk)
        
        print(request.user)
        
        form = CommentForm(request.POST)
        if form.is_valid():
            new_comment = form.save(commit=False)
            new_comment.author = request.user
            new_comment.post = post
            new_comment.save()
        
        comments = Comment.objects.filter(post=post).order_by('-created')
        
        context = {
            'post': post,
            'form': form,
            'comments': comments,
        }
        return render(request, 'social/post_detail.html', context)


class PostEditView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    
    model = Post
    fields = ['content']
    template_name = 'social/post_edit.html'
    
    def get_success_url(self):
        return reverse_lazy('post-detail', kwargs={'pk': self.kwargs['pk']})
    
    def test_func(self):
        post = self.get_object()
        return (self.request.user == post.author)


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    
    model = Post
    template_name = 'social/post_delete.html'
    success_url = reverse_lazy('posts')
    
    def test_func(self):
        post = self.get_object()
        return (self.request.user == post.author)


class CommentEditView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    
    model = Comment
    fields = ['comment']
    template_name = 'social/comment_edit.html'
    
    def get_success_url(self):
        return reverse_lazy('post-detail', kwargs={'pk': self.kwargs['post_pk']})
    
    def test_func(self):
        comment = self.get_object()
        return (self.request.user == comment.author)


class CommentDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    
    model = Comment
    template_name = 'social/comment_delete.html'
    
    def get_success_url(self):
        return reverse_lazy('post-detail', kwargs={'pk': self.kwargs['post_pk']})
    
    def test_func(self):
        comment = self.get_object()
        return (self.request.user == comment.author)
