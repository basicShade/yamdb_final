from django.core.exceptions import ValidationError
from django.db.models import Avg
from django.shortcuts import get_object_or_404
from rest_framework import serializers
from rest_framework.relations import SlugRelatedField
from rest_framework.fields import IntegerField

from reviews.models import Category, Comment, Genre, Review, Title


class CategorySerializer(serializers.ModelSerializer):
    """Сериализатор категорий"""

    class Meta:
        model = Category
        fields = ('name', 'slug')
        lookup_field = 'slug'


class GenreSerializer(serializers.ModelSerializer):
    """Сериализатор жанров"""

    class Meta:
        model = Genre
        fields = ('name', 'slug')
        lookup_field = 'slug'


class TitleWriteSerializer(serializers.ModelSerializer):
    """Сериализатор произведений - запись"""
    category = SlugRelatedField(
        required=True,
        slug_field='slug',
        queryset=Category.objects.all()
    )
    genre = SlugRelatedField(
        many=True,
        required=True,
        slug_field='slug',
        queryset=Genre.objects.all()
    )
    year = IntegerField(required=True)

    class Meta:
        model = Title
        fields = ('id', 'name', 'year', 'description', 'genre', 'category')


class TitleReadSerializer(serializers.ModelSerializer):
    """Сериализатор произведений - чтение"""
    category = CategorySerializer(read_only=True)
    genre = GenreSerializer(read_only=True, many=True)
    rating = serializers.SerializerMethodField()

    class Meta:
        model = Title
        fields = ('id', 'name', 'year', 'rating', 'description', 'genre',
                  'category'
                  )

    def get_rating(self, obj):
        return obj.reviews.aggregate(Avg('score')).get('score__avg')


class ReviewSerializer(serializers.ModelSerializer):
    """Сериализатор обзоров"""
    title = serializers.SlugRelatedField(
        slug_field='name',
        read_only=True
    )
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True
    )

    def validate_score(self, value):
        """Оценка"""
        if not 0 < value <= 10:
            raise serializers.ValidationError('Оценка по 10-бальной шкале!')
        return value

    def validate(self, data):
        """Валидация"""
        request = self.context['request']
        author = request.user
        title_id = self.context.get('view').kwargs.get('title_id')
        title = get_object_or_404(Title, pk=title_id)
        if (
            request.method == 'POST'
            and Review.objects.filter(title=title, author=author).exists()
        ):
            raise ValidationError('Может существовать только один отзыв!')
        return data

    class Meta:
        fields = '__all__'
        model = Review


class CommentSerializer(serializers.ModelSerializer):
    """Сериализатор комментариев"""
    review = serializers.SlugRelatedField(
        slug_field='text',
        read_only=True
    )
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True
    )

    class Meta:
        fields = '__all__'
        model = Comment
