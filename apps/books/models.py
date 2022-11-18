from random import randint
from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse


from slugify import slugify
from .parsing import get_db



User = get_user_model()


class Genre(models.Model):
    title = models.CharField(max_length=200, unique=True, db_index=True)
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
    title = models.CharField(max_length=200, db_index=True, primary_key=True)
    slug = models.SlugField(max_length=200, db_index=True)
    description = models.TextField(blank=True)
    year = models.PositiveIntegerField()
    language = models.CharField(max_length=7, choices=LANGUAGE_CHOICES, default='русский')
    price = models.PositiveSmallIntegerField()
    discount = models.BooleanField(default=False)
    discount_price = models.PositiveSmallIntegerField()
    pages = models.PositiveIntegerField(default=1)
    weight = models.PositiveSmallIntegerField()
    image = models.ImageField(upload_to='media/books_images/%Y/%m/%d', blank=True, null=True)
    image_link = models.CharField(max_length=1000, blank=True, null=True)
    stock = models.PositiveIntegerField()
    available = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)
        
    class Meta:
        verbose_name = 'Книга'
        verbose_name_plural = 'Книги'
        ordering = ('title',)
        index_together = (('title', 'slug'))

    def get_absolute_url(self):
        return reverse('post-detail', kwargs={'pk': self.pk})


class BookImage(models.Model):
    image = models.ImageField(upload_to='books_images/carousel')
    book = models.ForeignKey(
        to=Book,
        on_delete=models.CASCADE,
        related_name='book_images'
    )

    def __str__(self) -> str:
        return f'Image to {self.book.title}'


# db = get_db('ABC')


# for i in db:
#     book = Book.objects.create(
#             user = User.objects.get(username='admin'),
#             genre = Genre.objects.get(title='ABC'),
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
    
