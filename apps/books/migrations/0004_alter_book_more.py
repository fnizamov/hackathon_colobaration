# Generated by Django 4.1.3 on 2022-11-23 00:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0003_alter_book_more_alter_book_views_count'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='more',
            field=models.SlugField(blank=True, max_length=300),
        ),
    ]
