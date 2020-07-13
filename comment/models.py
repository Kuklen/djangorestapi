from django.utils import timezone

from django.contrib.auth.models import User
from django.db import models

# Create your models here.
from post.models import Post


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='post')
    content = models.TextField()
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='replies')  # yorumun altına yorum atılması için
    created = models.DateTimeField(editable=False)

    class Meta:
        ordering = ('created',)  # oluşturulma tarihine göre yorumları sıralamak için

    def __str__(self):
        return self.post.title + " " + self.user.username   #commenta tıkladığımızda yorumların bu şekilde gözükmesi için

    def save(self, *args,
             **kwargs):
        if not self.id:
            self.created = timezone.now()
        self.modified = timezone.now()
        return super(Comment, self).save(*args, **kwargs)


    def children(self):
        return Comment.objects.filter(parent=self)  #yorumların altında yorumları bulmamızı sağlıyacak

    @property
    def any_children(self):
        return Comment.objects.filter(parent=self).exists()  #içi içe yorumlarda altımızda herhangi bir yorum varmı ona bakıyoruz.




