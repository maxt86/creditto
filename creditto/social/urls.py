from django.urls import path

from .views import SearchView
from .views import ProfileView
from .views import ProfileEditView
from .views import FollowView
from .views import UnfollowView
from .views import FollowersView
from .views import ProfileNotificationView
from .views import PostsView
from .views import PostDetailView
from .views import PostEditView
from .views import PostDeleteView
from .views import PostNotificationView
from .views import LikeView
from .views import DislikeView
from .views import CommentReplyView
from .views import CommentEditView
from .views import CommentDeleteView
from .views import CommentLikeView
from .views import CommentDislikeView
from .views import NotificationDeleteView
from .views import ConversationsView
from .views import ThreadCreateView
from .views import ThreadView
from .views import ThreadNotificationView
from .views import MessageCreateView


urlpatterns = [
    path('', PostsView.as_view(), name='posts'),
    
    path('search/', SearchView.as_view(), name='search'),
    
    path('profile/<int:pk>/', ProfileView.as_view(), name='profile'),
    path('profile/<int:pk>/edit/', ProfileEditView.as_view(), name='profile-edit'),
    path('profile/<int:pk>/follow/', FollowView.as_view(), name='add-follower'),
    path('profile/<int:pk>/unfollow/', UnfollowView.as_view(), name='remove-follower'),
    path('profile/<int:pk>/followers/', FollowersView.as_view(), name='followers'),
    path('profile/<int:profile_pk>/notified/<int:pk>/', ProfileNotificationView.as_view(), name='profile-notification'),
    
    path('post/<int:pk>/', PostDetailView.as_view(), name='post-detail'),
    path('post/<int:pk>/edit/', PostEditView.as_view(), name='post-edit'),
    path('post/<int:pk>/delete/', PostDeleteView.as_view(), name='post-delete'),
    path('post/<int:pk>/like/', LikeView.as_view(), name='like'),
    path('post/<int:pk>/dislike/', DislikeView.as_view(), name='dislike'),
    path('post/<int:post_pk>/notified/<int:pk>', PostNotificationView.as_view(), name='post-notification'),
    
    path('post/<int:post_pk>/comment/<int:pk>/reply/', CommentReplyView.as_view(), name='comment-reply'),
    path('post/<int:post_pk>/comment/<int:pk>/edit/', CommentEditView.as_view(), name='comment-edit'),
    path('post/<int:post_pk>/comment/<int:pk>/delete/', CommentDeleteView.as_view(), name='comment-delete'),
    path('post/<int:post_pk>/comment/<int:pk>/like/', CommentLikeView.as_view(), name='comment-like'),
    path('post/<int:post_pk>/comment/<int:pk>/dislike/', CommentDislikeView.as_view(), name='comment-dislike'),
    
    path('inbox/', ConversationsView.as_view(), name='conversations'),
    path('newthread/', ThreadCreateView.as_view(), name='thread-create'),
    path('thread/<int:pk>/', ThreadView.as_view(), name='thread'),
    path('thread/<int:thread_pk>/notified/<int:pk>/', ThreadNotificationView.as_view(), name='thread-notification'),
    path('thread/<int:pk>/newmessage/', MessageCreateView.as_view(), name='message-create'),
    
    path('notified/<int:pk>/', NotificationDeleteView.as_view(), name='notification-delete'),
]
