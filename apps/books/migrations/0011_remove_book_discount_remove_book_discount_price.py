# Generated by Django 4.1.3 on 2022-11-26 11:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0010_alter_book_image'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='book',
            name='discount',
        ),
        migrations.RemoveField(
            model_name='book',
            name='discount_price',
        ),
    ]
