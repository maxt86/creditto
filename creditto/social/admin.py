from django.contrib import admin

from .models import Profile
from .models import Post
from .models import Comment
from .models import Notification


admin.site.register(Profile)
admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(Notification)
