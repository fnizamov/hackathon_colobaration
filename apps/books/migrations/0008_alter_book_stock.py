# Generated by Django 4.1.3 on 2022-11-23 16:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0007_comment_alter_bookimage_image_commentimage'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='stock',
            field=models.PositiveIntegerField(),
        ),
    ]