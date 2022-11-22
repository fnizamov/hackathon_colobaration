from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import BookViewSet, GenreViewSet, BookGenreView


router = DefaultRouter()
router.register('books', BookViewSet, 'book')
router.register('genres', GenreViewSet, 'genre')
router.register('filters', BookGenreView, 'filter')

urlpatterns = [
    # path('', include('apps.review.urls'))
]
urlpatterns += router.urls