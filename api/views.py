from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticatedOrReadOnly, DjangoModelPermissions
from rest_framework.filters import SearchFilter, OrderingFilter

from .models import Genre, Book, Comment
from .serializers import GenreSerializer, BookSerializer, CommentSerializer
from .permissions import IsCommentOwner


class GenreViewSet(ModelViewSet):
    permission_classes = [DjangoModelPermissions]
    queryset = Genre.objects.all().select_related().only('name', 'description')
    serializer_class = GenreSerializer


class BookViewSet(ModelViewSet):
    permission_classes = [DjangoModelPermissions]
    queryset = Book.objects.all().prefetch_related('genre').defer('published_year', 'pages')
    serializer_class = BookSerializer


class CommentViewSet(ModelViewSet):
    permission_classes = [IsAuthenticatedOrReadOnly, IsCommentOwner]
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

