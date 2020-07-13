from rest_framework.generics import CreateAPIView, ListAPIView, UpdateAPIView, RetrieveAPIView
from rest_framework.mixins import DestroyModelMixin

from comment.api.paginations import CommentPagination
from comment.api.permissions import IsOwner
from comment.api.serializers import CommentCreateSerializer, CommentListSerializer, CommentUpdateDeleteSerializer
from comment.models import Comment


class CommentCreateAPIVİew(CreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentCreateSerializer
    def perform_create(self, serializer):  #herkes kendi kullanıcı adı ile yorum yapabilmesi için
        serializer.save(user=self.request.user)

class CommentListAPIVİew(ListAPIView):
    serializer_class = CommentListSerializer
    pagination_class = CommentPagination
    def get_queryset(self):
        queryset = Comment.objects.filter(parent= None)  #parent ı none olanların gözükmesini sağlıyorz.
        query =self.request.GET.get("q")
        if query:
            queryset = queryset.filter(post=query)
        return queryset


''' class CommentDeleteAPIVİew(DestroyAPIView):  # UpdateModelMixin, RetrieveModelMixin
    queryset = Comment.objects.all()
    serializer_class = CommentUpdateDeleteSerializer
    lookup_field = 'pk'
    permission_classes = [IsOwner]

     def put(self,request, *args, **kwargs):
           return self.update(request, *args, **kwargs)
       def get(self,request, *args, **kwargs):
           return self.retrieve(request, *args, **kwargs)
           
update ve delete komutlarını mixin ile tek bir sayfada topladık '''




class CommentUpdateAPIVİew(UpdateAPIView, RetrieveAPIView, DestroyModelMixin):
    queryset = Comment.objects.all()
    serializer_class = CommentUpdateDeleteSerializer
    lookup_field = 'pk'
    permission_classes = [IsOwner]

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


