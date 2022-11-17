from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import BookViewSet, GenreViewSet

router = DefaultRouter()
router.register('books', BookViewSet, 'book')
router.register('genres', GenreViewSet, 'genre')

urlpatterns = [
    # path('', include('apps.review.urls'))
]
urlpatterns += router.urls