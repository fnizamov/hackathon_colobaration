from django.db import models
from django.contrib.auth import get_user_model

from apps.books.models import Book

User = get_user_model()

class Comment(models.Model):
    user = models.ForeignKey(
        to=User,
        on_delete=models.CASCADE,
        related_name='comments'
    )
    text = models.TextField()
    book = models.ForeignKey(
        to=Book,
        on_delete=models.CASCADE,
        related_name='comments'        
    )
    created_at = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(
        upload_to='media/books_images/%Y/%m/%d',
        blank=True,
        null=True
    )

    def __str__(self):
        return f'Comment from {self.user.username} to {self.book.title}'


class CommentImage(models.Model):
    image = models.ImageField(upload_to='media/comment_images/carousel')
    comment = models.ForeignKey(
        to=Comment,
        on_delete=models.CASCADE,
        related_name='comment_images'
    )