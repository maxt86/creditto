# Generated by Django 4.1 on 2022-09-13 16:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('social', '0014_alter_message_image'),
    ]

    operations = [
        migrations.CreateModel(
            name='Image',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(blank=True, null=True, upload_to='uploads/postpics')),
            ],
        ),
        migrations.RemoveField(
            model_name='post',
            name='image',
        ),
        migrations.AddField(
            model_name='post',
            name='image',
            field=models.ManyToManyField(blank=True, to='social.image'),
        ),
    ]
