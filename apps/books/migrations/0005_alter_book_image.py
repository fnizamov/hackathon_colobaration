# Generated by Django 4.1.3 on 2022-11-23 13:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0004_alter_book_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='image',
            field=models.ImageField(blank=True, default='/home/hello/SUPER/hackathon_colobaration/defoult_img/29302.png', null=True, upload_to='media/books_images'),
        ),
    ]
