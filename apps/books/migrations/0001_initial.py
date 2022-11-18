# Generated by Django 4.1.3 on 2022-11-18 16:48

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Book',
            fields=[
                ('author', models.CharField(db_index=True, max_length=50)),
                ('title', models.CharField(db_index=True, max_length=200)),
                ('slug', models.SlugField(blank=True, max_length=200, primary_key=True, serialize=False)),
                ('description', models.TextField(blank=True)),
                ('year', models.PositiveIntegerField()),
                ('language', models.CharField(choices=[('russian', 'Русский'), ('english', 'English'), ('spanish', 'Spanish'), ('france', 'France'), ('germany', 'Germany')], default='русский', max_length=7)),
                ('price', models.PositiveSmallIntegerField()),
                ('discount', models.BooleanField(default=False)),
                ('discount_price', models.PositiveSmallIntegerField(blank=True, null=True)),
                ('pages', models.PositiveIntegerField(default=1)),
                ('weight', models.PositiveSmallIntegerField()),
                ('image', models.ImageField(blank=True, null=True, upload_to='media/books_images/%Y/%m/%d')),
                ('image_link', models.CharField(blank=True, max_length=1000, null=True)),
                ('stock', models.PositiveIntegerField(default=1)),
                ('available', models.BooleanField(default=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'Книга',
                'verbose_name_plural': 'Книги',
                'ordering': ('title',),
            },
        ),
        migrations.CreateModel(
            name='Genre',
            fields=[
                ('title', models.CharField(db_index=True, max_length=200, primary_key=True, serialize=False, unique=True)),
                ('slug', models.SlugField(blank=True, max_length=200, unique=True)),
            ],
            options={
                'verbose_name': 'Жанр',
                'verbose_name_plural': 'Жанры',
                'ordering': ('title',),
            },
        ),
        migrations.CreateModel(
            name='BookImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='media/books_images/carousel')),
                ('book', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='book_images', to='books.book')),
            ],
        ),
        migrations.AddField(
            model_name='book',
            name='genre',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='books', to='books.genre'),
        ),
        migrations.AddField(
            model_name='book',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='books', to=settings.AUTH_USER_MODEL, verbose_name='Продавец'),
        ),
        migrations.AlterIndexTogether(
            name='book',
            index_together={('title', 'slug')},
        ),
    ]
