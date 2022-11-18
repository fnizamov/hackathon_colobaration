from dataclasses import fields
from email.policy import default
from requests import request
from rest_framework import serializers
from django.db.models import Avg

from .models import(
    Genre,
    Book,
    BookImage,
)

from apps.review.serializers import CommentSerializer


class BooksSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = Book
        exclude = ('discount', 'discount_price', 'stock')

    def validate_price(self, price):
        if price < 0:
            raise serializers.ValidationError('Цена не может быть отрицательной')
        return price

    def validate_quantity(self, quantity):
        if quantity < 0:
            raise serializers.ValidationError('Количество не может быть отрицательной')
        return quantity

    def validate(self, attrs):
        user = self.context['request'].user
        attrs['user'] = user
        return attrs

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['comments'] = CommentSerializer(instance.comments.all(), many=True).data
        representation['comments_count'] = instance.comments.all().count()
        return representation


class BooksListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ('title', 'genre', 'author', 'year', 'pages', 'language', 'price')

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['comments_count'] = instance.comments.all().count()
        return representation


class GenreListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ('title', 'slug')


class BookImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookImage
        fields = 'image',


class BookCreateSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(
        default=serializers.CurrentUserDefault(),
        source='user.username'
    )
    carousel_img = serializers.ListField(
        child=serializers.ImageField(),
        write_only=True
    )

    class Meta:
        model = Book
        fields = '__all__'


    def create(self, validated_data):
        carousel_images = validated_data.pop('carousel_img')
        book = Book.objects.create(**validated_data)
        images = []
        for image in carousel_images:
            images.append(BookImage(book=book, image=image))
        BookImage.objects.bulk_create(images)
        return book