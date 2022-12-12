from django.contrib import admin

from .models import Category, Genre, Title, Comment, Review


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """Админка категорий"""

    list_display = (
        'name',
        'slug',
    )
    search_fields = ('name',)
    empty_value_display = 'empty'


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    """Админка жанров"""

    list_display = (
        'name',
        'slug',
    )
    search_fields = ('name',)
    empty_value_display = 'empty'


@admin.register(Title)
class TitlesAdmin(admin.ModelAdmin):
    """Админка произведений"""

    list_display = (
        'name',
        'year',
        'description',
        'category',
    )
    search_fields = ('name',)
    list_filter = ('year',)
    empty_value_display = 'empty'


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    """Админка комментариев"""

    list_display = (
        'review',
        'text',
        'author',
        'pub_date',
    )
    search_fields = ('review__text',)
    list_filter = ('pub_date',)
    empty_value_display = 'empty'


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    """Админка обзоров"""

    list_display = (
        'title',
        'text',
        'author',
        'score',
    )
    search_fields = ('title__name',)
    list_filter = ('pub_date',)
    empty_value_display = 'empty'
