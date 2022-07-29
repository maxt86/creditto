from django.urls import path

from .views import PostsView
from .views import PostDetailView


urlpatterns = [
    path('', PostsView.as_view(), name='posts'),
    path('post/<int:pk>/', PostDetailView.as_view(), name='post-detail'),
]
