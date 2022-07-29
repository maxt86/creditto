from django.urls import path

from .views import PostsView
from .views import PostDetailView
from .views import PostEditView
from .views import PostDeleteView
from .views import CommentEditView
from .views import CommentDeleteView


urlpatterns = [
    path('', PostsView.as_view(), name='posts'),
    
    path('post/<int:pk>/', PostDetailView.as_view(), name='post-detail'),
    path('post/<int:pk>/edit/', PostEditView.as_view(), name='post-edit'),
    path('post/<int:pk>/delete/', PostDeleteView.as_view(), name='post-delete'),
    
    path('post/<int:post_pk>/comment/<int:pk>/edit/', CommentEditView.as_view(), name='comment-edit'),
    path('post/<int:post_pk>/comment/<int:pk>/delete/', CommentDeleteView.as_view(), name='comment-delete'),
]
