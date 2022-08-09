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


class Comment(models.Model):
    post = models.ForeignKey('Post', on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created = models.DateTimeField(default=timezone.now)
    comment = models.TextField()
