from django.contrib import admin
from .models import Comment, CommentImage


class TabularInLineImages(admin.TabularInline):
    model = CommentImage
    extra = 1
    fields = ['image']


class CommentAdmin(admin.ModelAdmin):
    model = Comment
    list_display = ['user', 'book', 'text']
    list_filter = ['user', 'book']
    inlines = [TabularInLineImages]

admin.site.register(Comment, CommentAdmin)