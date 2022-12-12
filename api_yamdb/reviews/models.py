from datetime import date

from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

User = get_user_model()


class Category(models.Model):
    """Модель категорий"""
    name = models.CharField(
        verbose_name='name',
        max_length=256,
    )
    slug = models.SlugField(
        verbose_name='slug',
        max_length=50,
        unique=True,
    )

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'
        ordering = ['name']

    def __str__(self):
        return self.slug


class Genre(models.Model):
    """Модель жанров"""
    name = models.CharField(
        verbose_name='name',
        max_length=256,
    )
    slug = models.SlugField(
        verbose_name='slug',
        max_length=50,
        unique=True,
    )

    class Meta:
        verbose_name = 'Genre'
        verbose_name_plural = 'Genres'
        ordering = ['name']

    def __str__(self):
        return self.slug


class Title(models.Model):
    """Модель произведения"""
    name = models.CharField(
        verbose_name='name',
        max_length=256,
    )
    year = models.IntegerField(
        verbose_name='year',
        blank=True,
        null=True,
        validators=[
            MinValueValidator(1),
            MaxValueValidator(date.today().year)],
    )
    description = models.TextField(
        blank=True,
        null=True
    )
    category = models.ForeignKey(
        Category,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        verbose_name='category',
        related_name='titles',
    )
    genre = models.ManyToManyField(Genre, through='GenreTitle')

    class Meta:
        verbose_name = 'Title'
        verbose_name_plural = 'Titles'
        ordering = ['-year']

    def __str__(self):
        return self.name


class GenreTitle(models.Model):
    genre = models.ForeignKey(
        Genre,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )
    title = models.ForeignKey(
        Title,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )

    def __str__(self) -> str:
        return f'{self.genre} {self.title}'


class Review(models.Model):
    """Модель обзоров."""
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        verbose_name='title',
        related_name='reviews',
    )
    text = models.CharField(
        max_length=700
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='author',
        related_name='reviews',
    )
    score = models.PositiveSmallIntegerField(
        verbose_name='score',
        validators=(
            MinValueValidator(1),
            MaxValueValidator(10)
        ),
        error_messages={'validators': 'Оценка от 1 до 10'}
    )
    pub_date = models.DateTimeField(
        verbose_name='publication date',
        auto_now_add=True,
        db_index=True
    )

    class Meta:
        verbose_name = 'Review'
        verbose_name_plural = 'Reviews'
        constraints = [
            models.UniqueConstraint(
                fields=('title', 'author', ),
                name='unique review'
            )]
        ordering = ('pub_date',)

    def __str__(self):
        return f'{self.title}, {self.score}, {self.author}'


class Comment(models.Model):
    """Модель комментариев."""
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        verbose_name='review',
        related_name='comments',
    )
    text = models.CharField(
        verbose_name='comment text',
        max_length=1500,
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='author',
        related_name='comments',
    )
    pub_date = models.DateTimeField(
        verbose_name='publication date',
        auto_now_add=True,
        db_index=True,
    )

    class Meta:
        verbose_name = 'Comment'
        verbose_name_plural = 'Comments'
        ordering = ('pub_date',)

    def __str__(self):
        return f'{self.author}, {self.pub_date}: {self.text[:15]}'
