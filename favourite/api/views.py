from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated

from favourite.api.paginations import FavouritePagination
from favourite.api.permissions import IsOwner
from favourite.api.serializers import FavouriteListCreateAPISerializer, FavouriteAPISerializer
from favourite.models import Favourite


class FavouriteListCreateAPIView(ListCreateAPIView):
    serializer_class = FavouriteListCreateAPISerializer
    pagination_class = FavouritePagination
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Favourite.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class FavouriteAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class = FavouriteAPISerializer
    queryset = Favourite.objects.all()
    lookup_field = "pk"
    permission_classes = [IsOwner]








