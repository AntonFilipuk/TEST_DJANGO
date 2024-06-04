from django.urls import path
from django.views.decorators.cache import cache_page

from app1.views import *

# сейчас мы будем декорировать класс представления через декоратор cache_page для хранения кэша
# 60 сек - хранится кэш (время кэширования)
# кэшируются только информационные сайты или страницы, которые обновляются редко, а не как чаты, динамически
# помогает разгрузить сервер
# cache_page(60)(EatHome.as_view())

urlpatterns = [
    path('', EatHome.as_view(), name="home"),
    path('about/', about, name='about'),
    path('addpage/', AddPage.as_view(), name='add_page'),
    path('contact/', ContactFormView.as_view(), name='contact'),
    path('login/', LoginUser.as_view(), name='login'),
    path('logout/', logout_user, name='logout'),
    path('register/', RegisterUser.as_view(), name='register'),
    # Если функция, то post_slug
    path('position/<slug:post_slug>/', ShowPost.as_view(), name='position'),
    path('category/<slug:category_slug>/', EatCategory.as_view(), name='category'),


]