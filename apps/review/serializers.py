from rest_framework import serializers
from .models import Comment, CommentImage


class CommentSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(
        default=serializers.CurrentUserDefault(),
        source='user.username'
    )
    carousel_img = serializers.ListField(
        child=serializers.ImageField(),
        write_only=True
    )
    class Meta:
        model = Comment
        fields = '__all__'

    def validate(self, attrs):
        user = self.context['request'].user
        attrs['user'] = user
        return attrs

    def create(self, validated_data):
        carousel_images = validated_data.pop('carousel_img')
        comment = Comment.objects.create(**validated_data)
        images = []
        for image in carousel_images:
            images.append(CommentImage(comment=comment, image=image))
        CommentImage.objects.bulk_create(images)
        return comment


class CommentImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = CommentImage
        fields = 'image',