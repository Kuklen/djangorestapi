from rest_framework import serializers
from rest_framework.serializers import ModelSerializer


from favourite.models import Favourite


class FavouriteListCreateAPISerializer(ModelSerializer):
    class Meta:
        model = Favourite
        fields = '__all__'

    def validate(self, attrs):   #favorilere eklendiyse bi daha eklenememesi için
        queryset = Favourite.objects.filter(post=attrs["post"], user=attrs["user"])
        if queryset.exists():
            raise serializers.ValidationError("Favorilere zaten eklendi")
        return attrs

class FavouriteAPISerializer(ModelSerializer):
    class Meta:
        model = Favourite
        fields = ('content',)









