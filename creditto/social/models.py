from enum import Enum

from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
    instance.profile.save()


class Profile(models.Model):
    
    user = models.OneToOneField(
        User,
        primary_key=True,
        verbose_name='user',
        related_name='profile',
        on_delete=models.CASCADE,
    )
    
    name = models.CharField(max_length=32, blank=True, null=True)
    birthdate = models.DateField(null=True, blank=True)
    location = models.CharField(max_length=128, blank=True, null=True)
    bio = models.TextField(max_length=512, blank=True, null=True)
    
    avatar = models.ImageField(
        upload_to='uploads/avatars',
        default='uploads/avatars/default.png',
        blank=True,
    )
    
    followers = models.ManyToManyField(User, related_name='followers', blank=True)


class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created = models.DateTimeField(default=timezone.now)
    content = models.TextField()
    likes = models.ManyToManyField(User, related_name='likes', blank=True)
    dislikes = models.ManyToManyField(User, related_name='dislikes', blank=True)


class Comment(models.Model):
    
    post = models.ForeignKey('Post', on_delete=models.CASCADE)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, related_name='+', blank=True, null=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created = models.DateTimeField(default=timezone.now)
    comment = models.TextField()
    likes = models.ManyToManyField(User, related_name='comment_likes', blank=True)
    dislikes = models.ManyToManyField(User, related_name='comment_dislikes', blank=True)
    
    @property
    def children(self):
        return Comment.objects.filter(parent=self).order_by('-created').all()
    
    @property
    def is_parent(self):
        return self.parent is None


NotificationType = Enum('NotificationType', 'LIKE COMMENT FOLLOW')

class Notification(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notification_from', null=True)
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notification_to', null=True)
    notification_type = models.IntegerField()
    date = models.DateTimeField(default=timezone.now)
    post = models.ForeignKey('Post', on_delete=models.CASCADE, related_name='+', blank=True, null=True)
    comment = models.ForeignKey('Comment', on_delete=models.CASCADE, related_name='+', blank=True, null=True)
    viewed = models.BooleanField(default=False)
