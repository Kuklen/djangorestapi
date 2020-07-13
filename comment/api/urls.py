from django.urls import path
from comment.api.views import CommentCreateAPIVİew, CommentListAPIVİew, CommentUpdateAPIVİew

app_name = "comment"
urlpatterns = [
    path('create', CommentCreateAPIVİew.as_view(), name='create'),
    path('list', CommentListAPIVİew.as_view(), name='list'),
   # path('delete/<pk>', CommentDeleteAPIVİew.as_view(), name='list'), update ile tek sayfada yaptığımız için kaldırdık
    path('update/<pk>', CommentUpdateAPIVİew.as_view(), name='list')
    ]