from django.contrib import admin
from .models import Post, Comment


#admin.site.register(Post)
@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    search_fields = ['title', 'body']
    list_display = ['title', 'author', 'created', 'status']
    list_filter =  ['title', 'author', 'created', 'status']

    raw_id_fields = ['author']
    #date_hierarchy = 'publish'     #publish ; created -> invalid datetime value
    ordering = ['created', 'author']


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    search_fields = ['post', 'author']
    list_display = ['post', 'author', 'content', 'created']
    list_filter =  ['post', 'author', 'created']

    raw_id_fields = ['author']
    ordering = ['created', 'post', 'author']
