# kullanıcı için izin sayfası oluşturduk ve izinleri burda belirliyoruz
from rest_framework.permissions import BasePermission

'''has_object_permission metoduyla biz login olan kullanıcıları yetkilendirdik ve login olmayan kullanıcıları o sayfaya girebiliyor delete işlemine tıklayabiliyor ve
   daha sonra yetkinliği olmadığı mesahı alıyordu. has_permission metodu ile biz login olmayan kullanıcıların hiçbir şekilde işlem yapmamasını sağlıyoruz yani login olmayan bir
   kullanıcı sayfaya ilk önce has_permission metodu tetiklenecek ve delete ve diğer butonları göremiyecek.'''
class NotAuthenticated(BasePermission):
    message = "You already have an account"
    def has_permission(self, request, view):
        return not request.user.is_authenticated

