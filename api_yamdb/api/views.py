from django.db.models import Avg
from django.shortcuts import get_object_or_404
from rest_framework import filters, viewsets
from reviews.models import Category, Genre, Review, Title
from .mixins import ModelMixinSet
from .permisions import (AdminModeratorAuthorPermission,
                         IsAdminUserOrReadOnly
                         )
from .serializers import CategorySerializer, GenreSerializer
from .serializers import CommentSerializer, ReviewSerializer
from .serializers import TitleReadSerializer, TitleWriteSerializer


class CategoryViewSet(ModelMixinSet):
    """View категорий"""
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name', )
    permission_classes = (IsAdminUserOrReadOnly, )
    lookup_field = 'slug'


class GenreViewSet(ModelMixinSet):
    """View жанров"""
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    permission_classes = (IsAdminUserOrReadOnly, )
    lookup_field = 'slug'


class TitleViewSet(viewsets.ModelViewSet):
    """View произведений"""
    permission_classes = (IsAdminUserOrReadOnly, )

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve'):
            return TitleReadSerializer
        return TitleWriteSerializer

    def get_queryset(self):
        qset = Title.objects.order_by('-year').annotate(Avg('reviews__score'))
        name = self.request.query_params.get('name')
        if name is not None:
            qset = qset.filter(name__icontains=name)

        year = self.request.query_params.get('year')
        if year is not None:
            qset = qset.filter(year=year)

        category = self.request.query_params.get('category')
        if category is not None:
            qset = qset.filter(category__slug__icontains=category)

        genre = self.request.query_params.get('genre')
        if genre is not None:
            qset = qset.filter(genre__slug__icontains=genre)

        return qset


class CommentViewSet(viewsets.ModelViewSet):
    """View комментариев"""
    serializer_class = CommentSerializer
    permission_classes = (AdminModeratorAuthorPermission,)

    def get_queryset(self):
        review = get_object_or_404(
            Review.objects.filter(title_id=self.kwargs.get('title_id')),
            id=self.kwargs.get('review_id'))
        return review.comments.all()

    def perform_create(self, serializer):
        review = get_object_or_404(
            Review.objects.filter(title_id=self.kwargs.get('title_id')),
            id=self.kwargs.get('review_id'))
        serializer.save(author=self.request.user, review=review)


class ReviewViewSet(viewsets.ModelViewSet):
    """View отзывов"""
    serializer_class = ReviewSerializer
    permission_classes = (AdminModeratorAuthorPermission,)

    def get_queryset(self):
        title = get_object_or_404(
            Title,
            id=self.kwargs.get('title_id'))
        return title.reviews.all()

    def perform_create(self, serializer):
        title = get_object_or_404(
            Title,
            id=self.kwargs.get('title_id'))
        serializer.save(author=self.request.user, title=title)
