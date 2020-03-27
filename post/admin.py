from django.contrib import admin

from .models import Post, Like

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    ordering = ('created_at', )
    list_display = ['id', 'content', ]

@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    ordering = ('updated_at', )
