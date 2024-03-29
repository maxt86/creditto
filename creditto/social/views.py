from django.db.models import Q

from django.utils import timezone

from django.http import HttpResponse

from django.shortcuts import render
from django.shortcuts import redirect

from django.urls import reverse_lazy

from django.contrib.auth.models import User

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.mixins import UserPassesTestMixin

from django.views import View
from django.views.generic.edit import UpdateView, DeleteView

from .models import Profile
from .models import Image
from .models import Post
from .models import Comment
from .models import NotificationType, Notification
from .models import Thread
from .models import Message

from .forms import PostForm
from .forms import CommentForm
from .forms import ThreadForm
from .forms import MessageForm
from .forms import ShareForm


class SearchView(View):
    
    MIN_QUERY_LEN = 4
    
    def get(self, request, *args, **kwargs):
        query = self.request.GET.get('q')
        
        if query is None or len(query) < self.MIN_QUERY_LEN:
            profiles = None
        else:
            profiles = Profile.objects.filter(
                Q(user__username__icontains=query)
            )
        
        context = {
            'profiles': profiles,
        }
        return render(request, 'social/search.html', context)


class ProfileView(View):
    
    def get(self, request, pk, *args, **kwargs):
        profile = Profile.objects.get(pk=pk)
        
        followers = profile.followers.all()
        num_followers = len(followers)
        
        following = False
        for follower in followers:
            if follower == request.user:
                following = True
                break
        
        user = profile.user
        posts = Post.objects.filter(Q(author=user) | Q(user_shared=user)).order_by('-created').order_by('-shared')
        
        context = {
            'profile': profile,
            'num_followers': num_followers,
            'following': following,
            'user': user,
            'posts': posts,
        }
        return render(request, 'social/profile.html', context)


class ProfileEditView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    
    model = Profile
    
    fields = [
        'avatar',
        'name',
        'birthdate',
        'location',
        'bio',
    ]
    
    template_name = 'social/profile_edit.html'
    
    def get_success_url(self):
        return reverse_lazy('profile', kwargs={'pk': self.kwargs['pk']})
    
    def test_func(self):
        profile = self.get_object()
        return (self.request.user == profile.user)


class FollowView(LoginRequiredMixin, View):
    
    def post(self, request, pk, *args, **kwargs):
        profile = Profile.objects.get(pk=pk)
        profile.followers.add(request.user)
        
        notification = Notification.objects.create(
            sender=request.user,
            receiver=profile.user,
            notification_type=NotificationType.FOLLOW.value,
        )
        
        return redirect('profile', pk=profile.pk)


class UnfollowView(LoginRequiredMixin, View):
    
    def post(self, request, pk, *args, **kwargs):
        profile = Profile.objects.get(pk=pk)
        profile.followers.remove(request.user)
        
        return redirect('profile', pk=profile.pk)


class FollowersView(View):
    
    def get(self, request, pk, *args, **kwargs):
        profile = Profile.objects.get(pk=pk)
        followers = profile.followers.all()
        
        context = {
            'profile': profile,
            'followers': followers,
        }
        return render(request, 'social/followers.html', context)


class ProfileNotificationView(LoginRequiredMixin, View):
    
    def get(self, request, profile_pk, pk, *args, **kwargs):
        notification = Notification.objects.get(pk=pk)
        
        if request.user != notification.receiver:
            return HttpResponse('failed', content_type='text/plain')
        
        notification.viewed = True
        notification.save()
        
        return redirect('profile', pk=profile_pk)


class PostsView(LoginRequiredMixin, View):
    
    def get(self, request, *args, **kwargs):
        posts = Post.objects.filter(
            Q(author__profile__followers__in=[request.user.id])
            & ~Q(user_shared=request.user)
        ).order_by('-created').order_by('-shared')
        
        form = PostForm()
        share_form = ShareForm()
        
        context = {
            'posts': posts,
            'form': form,
            'shareform': share_form,
        }
        return render(request, 'social/posts.html', context)
    
    def post(self, request, *args, **kwargs):
        posts = Post.objects.filter(
            author__profile__followers__in=[request.user.id]
        ).order_by('-created').order_by('-shared')
        
        files = request.FILES.getlist('image')
        
        form = PostForm(request.POST, request.FILES)
        share_form = ShareForm()
        
        if form.is_valid():
            new_post = form.save(commit=False)
            new_post.author = request.user
            new_post.save()
            
            for file in files:
                image = Image(image=file)
                image.save()
                new_post.image.add(image)
            
            new_post.save()
        
        context = {
            'posts': posts,
            'form': form,
            'shareform': share_form,
        }
        return render(request, 'social/posts.html', context)


class PostDetailView(View):
    
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
        
        if request.user != post.author:
            notification = Notification.objects.create(
                sender=request.user,
                receiver=post.author,
                notification_type=NotificationType.COMMENT.value,
                post=post,
            )
        
        context = {
            'post': post,
            'form': form,
            'comments': comments,
        }
        return render(request, 'social/post_detail.html', context)


class SharedPostView(View):
    
    def post(self, request, pk, *args, **kwargs):
        orig_post = Post.objects.get(pk=pk)
        
        form = ShareForm(request.POST)
        
        if form.is_valid():
            new_post = Post(
                author=orig_post.author,
                user_shared=request.user,
                created=orig_post.created,
                shared=timezone.now(),
                content=orig_post.content,
                shared_content=self.request.POST.get('content'),
            )
            
            new_post.save()
            
            for img in orig_post.image.all():
                new_post.image.add(img)
            
            new_post.save()
        
        return redirect('posts')


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


class PostNotificationView(LoginRequiredMixin, View):
    
    def get(self, request, post_pk, pk, *args, **kwargs):
        notification = Notification.objects.get(pk=pk)
        
        if request.user != notification.receiver:
            return HttpResponse('failed', content_type='text/plain')
        
        notification.viewed = True
        notification.save()
        
        return redirect('post-detail', pk=post_pk)


class LikeView(LoginRequiredMixin, View):
    
    def post(self, request, pk, *args, **kwargs):
        post = Post.objects.get(pk=pk)
        
        disliked = False
        for dislike in post.dislikes.all():
            if dislike == request.user:
                disliked = True
                break
        
        if disliked:
            post.dislikes.remove(request.user)
        
        liked = False
        for like in post.likes.all():
            if like == request.user:
                liked = True
                break
        
        if not liked:
            post.likes.add(request.user)
            
            if request.user != post.author:
                notification = Notification.objects.create(
                    sender=request.user,
                    receiver=post.author,
                    notification_type=NotificationType.LIKE.value,
                    post=post,
                )
        else:
            post.likes.remove(request.user)
        
        return HttpResponse(f'success {[-1, 1][not liked]} {int(disliked)}', content_type='text/plain')


class DislikeView(LoginRequiredMixin, View):
    
    def post(self, request, pk, *args, **kwargs):
        post = Post.objects.get(pk=pk)
        
        liked = False
        for like in post.likes.all():
            if like == request.user:
                liked = True
                break
        
        if liked:
            post.likes.remove(request.user)
        
        disliked = False
        for dislike in post.dislikes.all():
            if dislike == request.user:
                disliked = True
                break
        
        if not disliked:
            post.dislikes.add(request.user)
        else:
            post.dislikes.remove(request.user)
        
        return HttpResponse(f'success {[-1, 1][not disliked]} {int(liked)}', content_type='text/plain')


class CommentReplyView(LoginRequiredMixin, View):
    
    def post(self, request, post_pk, pk, *args, **kwargs):
        post = Post.objects.get(pk=post_pk)
        
        parent_comment = Comment.objects.get(pk=pk)
        
        form = CommentForm(request.POST)
        if form.is_valid():
            new_comment = form.save(commit=False)
            new_comment.author = request.user
            new_comment.parent = parent_comment
            new_comment.post = post
            new_comment.save()
        
        if request.user != parent_comment.author:
            notification = Notification.objects.create(
                sender=request.user,
                receiver=parent_comment.author,
                notification_type=NotificationType.COMMENT.value,
                comment=new_comment,
            )
        
        return redirect('post-detail', pk=post_pk)


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


class CommentLikeView(LoginRequiredMixin, View):
    
    def post(self, request, pk, *args, **kwargs):
        comment = Comment.objects.get(pk=pk)
        
        disliked = False
        for dislike in comment.dislikes.all():
            if dislike == request.user:
                disliked = True
                break
        
        if disliked:
            comment.dislikes.remove(request.user)
        
        liked = False
        for like in comment.likes.all():
            if like == request.user:
                liked = True
                break
        
        if not liked:
            comment.likes.add(request.user)
            
            if request.user != comment.author:
                notification = Notification.objects.create(
                    sender=request.user,
                    receiver=comment.author,
                    notification_type=NotificationType.LIKE.value,
                    comment=comment,
                )
        else:
            comment.likes.remove(request.user)
        
        next = request.POST.get('next', '/')
        return redirect(next)


class CommentDislikeView(LoginRequiredMixin, View):
    
    def post(self, request, pk, *args, **kwargs):
        comment = Comment.objects.get(pk=pk)
        
        liked = False
        for like in comment.likes.all():
            if like == request.user:
                liked = True
                break
        
        if liked:
            comment.likes.remove(request.user)
        
        disliked = False
        for dislike in comment.dislikes.all():
            if dislike == request.user:
                disliked = True
                break
        
        if not disliked:
            comment.dislikes.add(request.user)
        else:
            comment.dislikes.remove(request.user)
        
        next = request.POST.get('next', '/')
        return redirect(next)


class NotificationDeleteView(LoginRequiredMixin, View):
    
    def delete(self, request, pk, *args, **kwargs):
        notification = Notification.objects.get(pk=pk)
        
        if request.user != notification.receiver:
            return HttpResponse('failed', content_type='text/plain')
        
        notification.viewed = True
        notification.save()
        
        return HttpResponse('success', content_type='text/plain')


class ConversationsView(LoginRequiredMixin, View):
    
    def get(self, request, *args, **kwargs):
        threads = Thread.objects.filter(
            Q(user=request.user)
            | Q(receiver=request.user)
        )
        
        context = {
            'threads': threads,
        }
        return render(request, 'social/conversations.html', context)


class ThreadCreateView(LoginRequiredMixin, View):
    
    def get(self, request, *args, **kwargs):
        form = ThreadForm(initial={
            'username': self.request.GET.get('u', ''),
        })
        
        context = {
            'form': form,
        }
        return render(request, 'social/thread_create.html', context)
    
    def post(self, request, *args, **kwargs):
        form = ThreadForm(request.POST)
        
        username = request.POST.get('username')
        
        try:
            receiver = User.objects.get(username=username)
            
            if request.user == receiver:
                raise ValueError()
            
            if Thread.objects.filter(user=request.user, receiver=receiver).exists():
                thread = Thread.objects.filter(user=request.user, receiver=receiver)[0]
                return redirect('thread', pk=thread.pk)
            elif Thread.objects.filter(user=receiver, receiver=request.user).exists():
                thread = Thread.objects.filter(user=receiver, receiver=request.user)[0]
                return redirect('thread', pk=thread.pk)
            
            if form.is_valid():
                thread = Thread(
                    user=request.user,
                    receiver=receiver,
                )
                thread.save()
                
                return redirect('thread', pk=thread.pk)
        except:
            context = {
                'form': form,
                'errors': [
                    'Invalid username'
                ],
            }
            return render(request, 'social/thread_create.html', context)


class ThreadView(LoginRequiredMixin, View):
    
    def get(self, request, pk, *args, **kwargs):
        thread = Thread.objects.get(pk=pk)
        messages = Message.objects.filter(thread__pk__contains=pk)
        form = MessageForm()
        
        context = {
            'thread': thread,
            'messages': messages,
            'form': form,
        }
        return render(request, 'social/thread.html', context)


class ThreadNotificationView(LoginRequiredMixin, View):
    
    def get(self, request, thread_pk, pk, *args, **kwargs):
        notification = Notification.objects.get(pk=pk)
        
        if request.user != notification.receiver:
            return HttpResponse('failed', content_type='text/plain')
        
        thread = Thread.objects.get(pk=thread_pk)
        
        notification.viewed = True
        notification.save()
        
        return redirect('thread', pk=thread_pk)


class MessageCreateView(LoginRequiredMixin, View):
    
    def post(self, request, pk, *args, **kwargs):
        form = MessageForm(request.POST, request.FILES)
        
        thread = Thread.objects.get(pk=pk)
        
        if request.user == thread.receiver:
            receiver = thread.user
        else:
            receiver = thread.receiver
        
        if form.is_valid():
            message = form.save(commit=False)
            message.sender = request.user
            message.receiver = receiver
            message.thread = thread
            message.save()
            
            notification = Notification.objects.create(
                sender=request.user,
                receiver=receiver,
                notification_type=NotificationType.MESSAGE.value,
                thread=thread,
            )
        
        return redirect('thread', pk=pk)
