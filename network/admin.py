from django.contrib import admin
from .models import User, Profile, Post
# Register your models here.

class PagePost(admin.ModelAdmin):
    readonly_fields = ('created_at', 'user')

admin.site.register(User)
admin.site.register(Post, PagePost)
admin.site.register(Profile)
