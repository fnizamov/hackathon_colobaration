from django.contrib import admin

from .models import Genre, Book, BookImage, Comment, CommentImage


class CategoryAdmin(admin.ModelAdmin):
    list_display = ['title', 'slug']
    prepopulated_fields = {'slug': ('title',)}

admin.site.register(Genre, CategoryAdmin)

class TabularInLineImages(admin.TabularInline):
    model = CommentImage
    extra = 1
    fields = ['image']

class BookInLineImages(admin.TabularInline):
    model = BookImage
    extra = 1
    fields = ['image']


class BookAdmin(admin.ModelAdmin):
    model = Book
    search_fields = ['title']
    list_display = ['title', 'slug', 'price', 'stock', 'available', 'created', 'updated']
    list_filter = ['available', 'created', 'updated']
    list_editable = ['price', 'stock', 'available']
    prepopulated_fields = {'slug': ('title',)}
    inlines = [BookInLineImages]

admin.site.register(Book, BookAdmin)


class CommentAdmin(admin.ModelAdmin):
    model = Comment
    inlines = [TabularInLineImages]

admin.site.register(Comment, CommentAdmin)