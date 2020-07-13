# kullanıcı için izin sayfası oluşturduk ve izinleri burda belirliyoruz
from rest_framework.permissions import BasePermission

class IsOwner(BasePermission):
    #has_object_permission metoduyla biz login olan kullanıcıları yetkilendirdik ve login olmayan kullanıcıları o sayfaya girebiliyor delete işlemine tıklayabiliyor ve
    #daha sonra yetkinliği olmadığı mesahı alıyordu. has_permission metodu ile biz login olmayan kullanıcıların hiçbir şekilde işlem yapmamasını sağlıyoruz yani login olmayan bir
    #kullanıcı sayfaya ilk önce has_permission metodu tetiklenecek ve delete ve diğer butonları göremiyecek.
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated
    message= "You must be the owner of this object."
    def has_object_permission(self,request, view, obj):
        return (obj.user == request.user)