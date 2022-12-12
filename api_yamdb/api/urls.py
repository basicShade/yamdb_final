from django.urls import include, path
from rest_framework import routers

from .views import (CategoryViewSet, CommentViewSet, GenreViewSet,
                    ReviewViewSet, TitleViewSet
                    )

app_name = 'api'

router_v1 = routers.DefaultRouter()
router_v1.register(r'titles', TitleViewSet, basename='titles')
router_v1.register(r'categories', CategoryViewSet, basename='categories')
router_v1.register(r'genres', GenreViewSet, basename='genres')
router_v1.register(r'comments', CommentViewSet, basename='comments')
router_v1.register(
    (r'titles/(?P<title_id>[1-9]+[0-9]*)/reviews/'
     r'(?P<review_id>[1-9]+[0-9]*)/comments'
     ),
    CommentViewSet,
    basename='comments'
)
router_v1.register(
    r'titles/(?P<title_id>[1-9]+[0-9]*)/reviews',
    ReviewViewSet,
    basename='reviews'
)

urlpatterns = [
    path('v1/', include(router_v1.urls)),
]
