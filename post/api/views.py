from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.generics import ListAPIView,RetrieveAPIView,RetrieveUpdateAPIView,CreateAPIView
from rest_framework.mixins import DestroyModelMixin

from account.api.throttles import RegisterThrottle
from post.api.paginations import PostPagination
from post.api.serializers import PostSerializer,PostUpdateCreateSerializer
from post.models import Post
from rest_framework.permissions import IsAuthenticated
from post.api.permissions import IsOwner


class PostListAPIView(ListAPIView):
    #queryset = Post.objects.all()  #postların içindeki tüm quesyleri verileri getir demek oluyor.
    serializer_class = PostSerializer
    filter_backends = [SearchFilter, OrderingFilter]   # sıralama işlemleri orderinfilter
    search_fields = ['title', 'content']   # neye göre arama yapacağımızı belirttik.
    pagination_class = PostPagination
    def get_queryset(self):
        queryset = Post.objects.filter(draft=False)  #draft ta olmayan verileri get_queryset ile geri döndürdük
        return queryset


class PostDetailAPIView(RetrieveAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    lookup_field = 'slug'  #sluga göre gitmesi için

""" class PostDeleteAPIView(DestroyAPIView): #update in içine aldık mixinle
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    lookup_field = 'slug'
    permission_classes = [IsOwner] """

class PostUpdateAPIView(RetrieveUpdateAPIView, DestroyModelMixin):
    queryset = Post.objects.all()
    serializer_class = PostUpdateCreateSerializer
    lookup_field = 'slug'
    permission_classes = [IsOwner] # permissionstan aldık IsOwner objesini eğer kullanıcı postu oluşturmuşsa update edebilmesi için ve admin değiştirebilir.
    def perform_update(self,serializers):
        serializers.save(modified_by=self.request.user)
    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)

class PostCreateAPIView(CreateAPIView):
    queryset = Post.objects.all()  # lookup_field ı aramada kullandığımız için burada kullanmıyoruz
    serializer_class = PostUpdateCreateSerializer
    permission_classes = [IsAuthenticated]


    #  models.py de veritabanı kayıtlarının oluştururken created ve slug alanlarında editable=False yaptığımız için create sayfasında bu alanlar gözükmez
    # zaten biz bu alanların gözükmesini de istemeyiz o yüzden serializers kısmına ikinci bir serializers açar ve görünmesini istdeğimiz alanları belirtiriz.
    # serializers. PostUpdateCreateSerializera adında bir serializers daha açıp update ve create adımlarında serializers_class a bunları tanımladık.
    def perform_create(self, serializers):                    #oluşturulan postların oluşturulan kişiye özgü olması için
        serializers.save(user=self.request.user)







