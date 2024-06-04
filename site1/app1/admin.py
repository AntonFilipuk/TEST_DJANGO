from django.contrib import admin
from django.utils.safestring import mark_safe

# Register your models here.

from .models import *


class EatAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'time_create', 'get_html_photo', 'is_existed')
    list_display_links = ('id', 'title')
    search_fields = ('title',)
    list_editable = ('is_existed',)
    list_filter = ('time_create', 'is_existed')
    prepopulated_fields = {"slug": ("title",)}
    # Атрибут, который содержит порядок и список редактируемых полей. Именно уже когда статью изменяешь.
    fields = ('title', 'slug', 'category', 'description', 'photo', 'get_html_photo', 'is_existed', 'time_create', 'time_update')
    # поля в редакторе только для чтения
    readonly_fields = ('time_create', 'time_update', 'get_html_photo')
    # Метод, который панель сохранения вверх перемещает, чтобы вниз долго не крутить.
    # save_on_top = True
    # Метод, который будет формировать html код для отображения миниатюры.
    # Типа будет тэг img, который будет ссылаться на url изображения.
    # Object - будет ссылаться на текущую запись списка. Название метода придумываем сами.
    # Mark_safe - означает не экранировать тэги, чтобы они были рабочими и будут выполняться.
    def get_html_photo(self, object):
        if object.photo:
            return mark_safe(f"<img src='{object.photo.url}'width=50>")

    get_html_photo.short_description = 'Миниатюра'

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_display_links = ('id', 'name')
    search_fields = ('name',)
    prepopulated_fields = {"slug": ("name",)}


admin.site.register(Eat, EatAdmin)
admin.site.register(Category, CategoryAdmin)

# прописываем атрибуты для отображения в админке своих заголовков
admin.site.site_title = 'Админ-панель Пицулечка бай'
# это заголовок большой на странице
admin.site.site_header = 'Админ-панель Пицулечка бай'
