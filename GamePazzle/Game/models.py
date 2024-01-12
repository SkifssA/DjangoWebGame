from django.db import models

# Create your models here.
class Image(models.Model):
    name = models.CharField(max_length=255, null=False, blank=False, verbose_name=u'Имя пятнашек')
    file = models.ImageField(upload_to='imgs/', null=True, max_length=255, verbose_name=u'Файл')

    def __repr__(self):
        return f'Img({self.name}, {self.file})'

    def __str__(self):
        return self.name