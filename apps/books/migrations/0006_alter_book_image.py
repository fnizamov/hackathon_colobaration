# Generated by Django 4.1.3 on 2022-11-23 13:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0005_alter_book_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='image',
            field=models.ImageField(blank=True, default='default/29302.png', upload_to='post_images'),
        ),
    ]
