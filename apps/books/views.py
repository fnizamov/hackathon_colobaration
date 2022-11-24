from rest_framework import mixins, status, filters
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters import rest_framework as rest_filter


from .models import (
    Genre,
    Book,
)

from .serializers import (
    GenreListSerializer,
    BooksListSerializer,
    BooksSerializer,
    BookCreateSerializer,
    # BookImageSerializer,
    CommentSerializer
)

from .permissions import IsOwner


class ProductFilter(rest_filter.FilterSet):
    max_price = rest_filter.NumberFilter(field_name="price", lookup_expr='lt')
    min_price = rest_filter.NumberFilter(field_name="price", lookup_expr='gt')

    class Meta:
        model = Book
        fields = ['genre',]


class BookGenreView(ModelViewSet):
    queryset = Book.objects.filter(genre__title='Fantasy')
    serializer_class = BooksListSerializer


class GenreViewSet(ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreListSerializer

    filter_backends = [
        filters.SearchFilter,
        rest_filter.DjangoFilterBackend,
        filters.OrderingFilter
    ]
    search_fields = ['title']
    filterset_fields = ['slug']
    ordering_fields = ['created']

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_serializer_class(self):
        if self.action == 'list':
            return GenreListSerializer
        elif self.action == 'create':
            return BookCreateSerializer
        return super().get_serializer_class()

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            self.permission_classes = [AllowAny]
        if self.action in ['create']:
            self.permission_classes = [IsAuthenticated]
        if self.action in ['destroy', 'update', 'partial_update']:
            self.permission_classes = [IsOwner]
        return super().get_permissions()


class BookViewSet(ModelViewSet):
    queryset = Book.objects.all()
    filter_backends = [
        filters.SearchFilter,
        rest_filter.DjangoFilterBackend,
        filters.OrderingFilter,
    ]
    search_fields = ['title', 'genre__title']
    filterset_fields = ['slug']
    ordering_fields = ['created']
    filterset_class = ProductFilter
    
    def get_serializer_class(self):
        if self.action == 'list':
            return BooksListSerializer
        return BooksSerializer

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context

    def get_permissions(self):
        if self.action == 'create':
            self.permission_classes = [IsAuthenticated]
        return super().get_permissions()

    def retrieve(self, request, *args, **kwargs):
        instance: Book = self.get_object() # Product
        instance.views_count += 1
        instance.save()
        return super().retrieve(request, *args, **kwargs)


    @action(detail=True, methods=['POST', 'DELETE'])
    def comment(self, request, pk=None):
        book = self.get_object()
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(user=request.user, book=book)
            return Response(
                serializer.data, status=status.HTTP_201_CREATED
                )