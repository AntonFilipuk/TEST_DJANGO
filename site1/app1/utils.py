from django.db.models import Count
from django.core.cache import cache

# Этот файл предназначен, чтобы выносить сюда всю общую информацию
# и исключать дублирование
from app1.models import *

menu = [{'title': "О нас", 'url_name': 'about'},
        {'title': "Добавить рецепт", 'url_name': 'add_page'},
        {'title': "Обратная связь", 'url_name': 'contact'},
        ]


class DataMixin:
    paginate_by = 3

    def get_user_context(self, **kwargs):
        # делаем распаковку словаря kwargs и получаем весь контекст который на данный момент сформирован
        context = kwargs

        # API низкоуровневого кэширования
        # Если присутствует коллекция cats, то берем отсюда, если нет, то читаем с бд и заносим в кэш, в следующий
        # раз возьмем ее из кэша

        cats = cache.get("cats")
        if not cats:
            # Количество постов, связанных с этой рубрикой
            # считает сколько в каждой рубрике постов
            cats = Category.objects.annotate(Count('get_posts'))
            cache.set("cats", cats, 60)

        user_menu = menu.copy()
        if not self.request.user.is_authenticated:
            user_menu.pop(1)  # удаляем Добавить рецепт из меню, если пользователь не авторизован
        context['menu'] = user_menu
        context['cats'] = cats
        if 'cat_selected' not in context:
            context['cat_selected'] = 0
        return context