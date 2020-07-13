from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.utils.text import slugify
# Create your models here.

class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,default=1)  # cascade bir kullanıcıyı silersek onla ilişkili diğer şeylerinde silinmesi işine yarar.
    title = models.CharField(max_length=120)
    content = models.TextField()
    draft = models.BooleanField(default=False)  #taslaklara kaydetmek için
    created = models.DateTimeField(editable=False)  # oluşturulma tarihi
    modified = models.DateTimeField()   #değiştirilme tarihi
    slug = models.SlugField(unique=True, max_length=150, editable=False) #daha anlamlı SEO açısından daha düzgün url ler sağlamak için
    image = models.ImageField(upload_to='post', null=True, blank=True)
    modified_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='modified_by') #kimin tarafından düzenlendiği
    class Meta:
        ordering = ["-id"]
    def get_slug(self):
        slug = slugify(self.title.replace("ı", "i"))  #title ın içinde ı varsa i ye çevir ve slugifyla url açısından
        unique = slug
        number = 1
         
        while Post.objects.filter(slug=unique).exists(): #eğer örnek hasan diye bi kayıt varsa bunun yerine hasan-1 ve hasan-2 gibi kayıtları oluşturucak
             unique = '{}-{}'.format(slug, number)
             number += 1
        return unique


    def __str__(self):
        return self.title


    
    def save(self, *args, **kwargs): #eğer ilk defa post oluşturuluyorsa id hazır değildir o yüzden created=timezono.now() gerçekleştirilir.
        if not self.id:              #ama sonraki düzenlemelerde buraya girmiyecektir çünkü o verinin bir id si olmuş oluyor.
            self.created = timezone.now()
        self.modified = timezone.now() #her bir değişiklik olduğunda buradaki saatide değiştireceğimiz anlamı taşıyor.
        self.slug = self.get_slug() #kayıt esnasında slug değerinin def fonksiyonu içinde hasan-1 hasan-2 şeklinde olmasını sağlıyoruz
        return super(Post, self).save(*args, **kwargs)
