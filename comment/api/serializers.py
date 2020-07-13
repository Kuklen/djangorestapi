from django.contrib.auth.models import User
from rest_framework.serializers import ModelSerializer, SerializerMethodField
from comment.models import Comment
from rest_framework import serializers

from post.models import Post


class CommentCreateSerializer(ModelSerializer):
    class Meta:
        model = Comment
        exclude = ['created', ]  #var olan bütün fieldleri çağırıyor created hariç

    def validate(self, attrs):   #bir konunun içinde yorumlara başka bir konu başlığıyla yorum yapamamak için örnek 1. konudaki bir yoruma 2.konudan yorum yapmak
        if (attrs["parent"]):
            if attrs["parent"].post != attrs["post"]:  # parent ın konusuyla post aynı olmalı. aynı değilse hata vericek
                raise serializers.ValidationError("something went wrong")
        return attrs



class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'id', 'email')

class PostCommentSerializer(ModelSerializer):
    class Meta:
        model = Post
        fields = ('title', 'slug', 'id')


class CommentListSerializer(ModelSerializer):
    replies = SerializerMethodField()
    user = UserSerializer()
    post = PostCommentSerializer()
    class Meta:
        model = Comment
        fields = '__all__'
       # depth = 1 bütün herşeyi getirir bunu koyarsak userın altına
    def get_replies(self, obj):
        if obj.any_children:
            return CommentListSerializer(obj.children(), many=True).data

class CommentUpdateDeleteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = [
            'content'
        ]








