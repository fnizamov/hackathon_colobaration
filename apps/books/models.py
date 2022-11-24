from random import randint
from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse


from slugify import slugify
from .parsing import get_db
from .utils import get_time


User = get_user_model()


class Genre(models.Model):
    title = models.CharField(max_length=200, unique=True, db_index=True, primary_key=True)
    slug = models.SlugField(max_length=200, db_index=True, unique=True, blank=True)

    def __str__(self) -> str:
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    class Meta:
        ordering = ('title',)
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'

class Book(models.Model):
    LANGUAGE_CHOICES = (
        ('russian', 'Русский'),
        ('english', 'English'),
        ('spanish', 'Spanish'),
        ('france', 'France'),
        ('germany', 'Germany')
    )

    user = models.ForeignKey(
        verbose_name='Продавец',
        to=User,
        on_delete=models.CASCADE,
        related_name='books'
    )
    genre = models.ForeignKey(Genre, related_name='books', on_delete=models.CASCADE)
    author = models.CharField(max_length=50, db_index=True)
    title = models.CharField(max_length=200, db_index=True)
    slug = models.SlugField(max_length=200, db_index=True, blank=True, primary_key=True)
    description = models.TextField(blank=True)
    year = models.PositiveIntegerField()
    language = models.CharField(max_length=7, choices=LANGUAGE_CHOICES, default='русский')
    price = models.PositiveSmallIntegerField()
    discount = models.BooleanField(default=False)
    discount_price = models.PositiveSmallIntegerField(blank=True, null=True)
    pages = models.PositiveIntegerField()
    weight = models.PositiveSmallIntegerField()
    image = models.ImageField(upload_to='post_images', blank=True, default='default/29302.png')
    image_link = models.CharField(max_length=1000, blank=True, null=True)
    stock = models.PositiveIntegerField()
    available = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    views_count = models.IntegerField(default=0, blank=True)
    more = models.SlugField(max_length=300, db_index=True, blank=True)

    def __str__(self) -> str:
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title + get_time())
            self.more = f'http://127.0.0.1:8000/market/books/{self.slug}'
        super().save(*args, **kwargs)
        
    class Meta:
        verbose_name = 'Книга'
        verbose_name_plural = 'Книги'
        ordering = ('title',)
        index_together = (('title', 'slug'))

    def get_absolute_url(self):
        return reverse('post-detail', kwargs={'pk': self.pk})


class BookImage(models.Model):
    image = models.ImageField(upload_to='carousel')
    book = models.ForeignKey(
        to=Book,
        on_delete=models.CASCADE,
        related_name='book_images'
    )

    def __str__(self) -> str:
        return f'Image to {self.book.title}'



class Comment(models.Model):
    ONE = 1
    TWO = 2
    THREE = 3
    FOUR = 4
    FIVE = 5
    RAITING_CHOICES = (
        (ONE, '1'),
        (TWO, '2'),
        (THREE, '3'),
        (FOUR, '4'),
        (FIVE, '5')
    )
    user = models.ForeignKey(
        to=User,
        on_delete=models.CASCADE,
        related_name='comments'
    )
    book = models.ForeignKey(
        to=Book,
        on_delete=models.CASCADE,
        related_name='comments'
    )
    rating = models.PositiveSmallIntegerField(
        choices=RAITING_CHOICES,
        blank=True,
        null=True)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'

    def __str__(self) -> str:
        return f'Comment from {self.user.username} to {self.book.title}'


class CommentImage(models.Model):
    image = models.ImageField(upload_to='media/comment_images/carousel')
    comment = models.ForeignKey(
        to=Comment,
        on_delete=models.CASCADE,
        related_name='comment_images'
    )

    def str(self) -> str:
        return f'Image to {self.comment.book}'


# db = get_db('CYBERPUNK')


# for i in db:
#     book = Book.objects.create(
#             user = User.objects.get(username='admin'),
#             genre = Genre.objects.get(title='Cyberpank'),
#             author = i['author'],
#             title = i['title'],
#             description = i['desc'],
#             year= randint(1950, 2022),
#             price = randint(200, 2000),
#             discount_price = randint(1, 50),
#             pages = randint(1, 1000),
#             weight = randint(100, 900),
#             image_link = i['photo'],
#             stock = randint(100, 300)
#             )
    
