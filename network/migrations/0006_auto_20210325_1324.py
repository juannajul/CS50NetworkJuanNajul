# Generated by Django 3.0.8 on 2021-03-25 17:24

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0005_auto_20210305_0117'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='likes',
            field=models.ManyToManyField(default=None, related_name='post_likes', to=settings.AUTH_USER_MODEL),
        ),
    ]
