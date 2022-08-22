from django.urls import path

from .views import SearchView
from .views import ProfileView
from .views import ProfileEditView
from .views import FollowView
from .views import UnfollowView
from .views import PostsView
from .views import PostDetailView
from .views import PostEditView
from .views import PostDeleteView
from .views import LikeView
from .views import DislikeView
from .views import CommentEditView
from .views import CommentDeleteView


urlpatterns = [
    path('', PostsView.as_view(), name='posts'),
    
    path('search/', SearchView.as_view(), name='search'),
    
    path('profile/<int:pk>/', ProfileView.as_view(), name='profile'),
    path('profile/<int:pk>/edit/', ProfileEditView.as_view(), name='profile-edit'),
    path('profile/<int:pk>/follow', FollowView.as_view(), name='add-follower'),
    path('profile/<int:pk>/unfollow', UnfollowView.as_view(), name='remove-follower'),
    
    path('post/<int:pk>/', PostDetailView.as_view(), name='post-detail'),
    path('post/<int:pk>/edit/', PostEditView.as_view(), name='post-edit'),
    path('post/<int:pk>/delete/', PostDeleteView.as_view(), name='post-delete'),
    path('post/<int:pk>/like', LikeView.as_view(), name='like'),
    path('post/<int:pk>/dislike', DislikeView.as_view(), name='dislike'),
    
    path('post/<int:post_pk>/comment/<int:pk>/edit/', CommentEditView.as_view(), name='comment-edit'),
    path('post/<int:post_pk>/comment/<int:pk>/delete/', CommentDeleteView.as_view(), name='comment-delete'),
]
