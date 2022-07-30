# Generated by Django 4.0.6 on 2022-07-30 18:17

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        ('social', '0004_alter_comment_created_alter_post_created'),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, related_name='profile', serialize=False, to=settings.AUTH_USER_MODEL, verbose_name='user')),
                ('name', models.CharField(blank=True, max_length=32, null=True)),
                ('birthdate', models.DateField(blank=True, null=True)),
                ('location', models.CharField(blank=True, max_length=128, null=True)),
                ('bio', models.TextField(blank=True, max_length=512, null=True)),
                ('avatar', models.ImageField(blank=True, default='uploads/avatars/default.png', upload_to='uploads/avatars')),
            ],
        ),
    ]
