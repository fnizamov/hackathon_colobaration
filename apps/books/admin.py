from django.contrib import admin

from .models import Genre, Book, BookImage

# admin.site.register((Tag, Comment))

class CategoryAdmin(admin.ModelAdmin):
    list_display = ['title', 'slug']
    prepopulated_fields = {'slug': ('title',)}

admin.site.register(Genre, CategoryAdmin)

class TabularInLineImages(admin.TabularInline):
    model = BookImage
    extra = 1
    fields = ['image']

class BookAdmin(admin.ModelAdmin):
    model = Book
    list_display = ['title', 'slug', 'price', 'stock', 'available', 'created', 'updated']
    list_filter = ['available', 'created', 'updated', 'discount']
    list_editable = ['price', 'stock', 'available']
    prepopulated_fields = {'slug': ('title',)}
    inlines = [TabularInLineImages]

admin.site.register(Book, BookAdmin)