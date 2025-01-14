from django.db import models
from django.urls import reverse


# Create your models here.

class Eat(models.Model):
    title = models.CharField(max_length=255, verbose_name='Заголовок')
    description = models.TextField(blank=True, verbose_name='Описание')
    photo = models.ImageField(upload_to='photos/%Y/%m/%d', verbose_name='Фото')
    time_create = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    time_update = models.DateTimeField(auto_now=True, verbose_name='Дата изменения')
    is_existed = models.BooleanField(default=True, verbose_name='Наличие')
    # Например <object>.category_id будет лежать номер категории, а <object>.category - будет хранить экземпляр класса Category с этим id именно
    category = models.ForeignKey('Category', on_delete=models.PROTECT, verbose_name='Категория', related_name='get_posts')
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name='URL')

    # Нужен для отображения записей в QuerySet ни как экземпляров типа Eat object (1), а например по заголовку
    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('position', kwargs={'post_slug': self.slug})

    class Meta:
        verbose_name = 'Все позиции еды'
        verbose_name_plural = 'Все позиции еды'
        ordering = ['-time_create', 'title']


class Category(models.Model):
    name = models.CharField(max_length=100, db_index=True, verbose_name='Категория')
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name='URL')

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('category', kwargs={'category_slug': self.slug})

    class Meta:
        verbose_name = 'Категории'
        verbose_name_plural = 'Категории'
        ordering = ['id']
