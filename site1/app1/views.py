from django.contrib.auth import logout, login
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.views import LoginView
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseNotFound
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, FormView
from django.contrib.auth.mixins import LoginRequiredMixin

from app1.forms import *
from app1.models import *
from app1.utils import *


# класс, отвечающий за главную страницу нашего сайта
class EatHome(DataMixin, ListView):
    # paginate_by = 3 # разбивка по 3 поста на стр
    # <имя приложения>/<имя модели> list.html
    model = Eat  # выбирает все записи из таблицы и пытается их отобразить в виде списка
    template_name = 'app1/index.html'
    context_object_name = 'posts'  # чтобы использовать posts, по дефолту object_list

    # extra_context = {'title': 'Главная страница'} #можно передавать только неизменяемые значения

    #  формируем функцию, чтобы передать главное меню menu, потому что это изменяемый объект
    def get_context_data(self, *, object_list=None, **kwargs):
        # Получаем весь контекст, который уже сформирован, например, posts уже существует.
        # Вынимаем context_object
        # делаем распаковку словаря kwargs и получаем весь контекст который на данный момент сформирован

        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Главная страница")
        #  Объединяем эти два словаря:
        return dict(list(context.items()) + list(c_def.items()))

    # переписали model, теперь отображает с фильтром на галочку 'существует'
    # так можно через админку прописывать статьи, которые отображать на сайте
    def get_queryset(self):
        return Eat.objects.filter(is_existed=True)

        # Пример жадного запроса, то есть который захватывает с собой еще данные котор пригодятся по пути
        # выполнения программы. А ленивый запрос делается всегда, то есть каждый раз обращается к базе данных даже
        # за одним полем, а это уже дубликат и нагружает базу

        # 'cat' - внешний(вторичный) ключ в таблице Eat что связывает Category и Eat
        # жадный запрос возьмет и все данные с таблицы Category и не будет выполняться дополнительного
        # ленивого запроса

        # return Eat.objects.filter(is_existed=True).select_related('cat')


# Create your views here.
# def index(request):
#     posts = Eat.objects.all()
#
#     context = {
#         'title': "Главная app1",
#         'menu': menu,
#         'posts': posts,
#         'cat_selected': 0}
#     # папку templates джанго находит сам
#     return render(request, 'app1/index.html', context=context)

def about(request):
    context = {
        'title': "О нас",
        'menu': menu,
    }
    print(request.GET)
    return render(request, 'app1/about.html', context=context)


class AddPage(LoginRequiredMixin, DataMixin, CreateView):
    form_class = AddPostForm  # класс формы, с которым будет связан AddPage
    template_name = 'app1/addpage.html'
    # используется , если нет absolute_url
    success_url = reverse_lazy('home')
    # поле для перенаправления, если не зареган
    # lazy чтобы мы могли использовать имена адресов
    login_url = reverse_lazy('home')

    # raise_exception = True
    def get_context_data(self, *, object_list=None, **kwargs):
        # этот контекст данных уже сформирован классом listview
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Добавление статьи")
        return dict(list(context.items()) + list(c_def.items()))


# def addpage(request):
#     if request.method == 'POST':
#         form = AddPostForm(request.POST, request.FILES)
#         if form.is_valid():
#             # print(form.cleaned_data)
#             # Добавление формы в базу данных, если она прошла валидность
#             # try:
#                 #Eat.objects.create(**form.cleaned_data)
#
#                 form.save() # все данные, которые будут переданы от формы будут автоматически занесены в базу
#                 # редирект на главную
#                 return redirect('home')
#             # except:
#                 # отображается общая ошибка, если что-то не так срвзу на экране красным
#                 # form.add_error(None, 'Ошибка добавления рецепта')
#     else:
#         # создаем экземпляр класса формы для заполнения из forms
#         form = AddPostForm()
#     return render(request, 'app1/addpage.html', {'form': form, 'menu': menu, 'title': 'Добавление рецепта'})


def pageNotFound(request, exception):
    return HttpResponseNotFound('<h1>Страница не найдена</h1>')


class ShowPost(DataMixin, DetailView):
    model = Eat
    template_name = 'app1/post.html'
    slug_url_kwarg = 'post_slug'
    # Если используется айдишник
    # pk_url_kwarg = 'pk'

    # куда будут перемещаться данные, взятые из модели
    context_object_name = 'post'

    def get_context_data(self, *, object_list=None, **kwargs):
        # этот контекст данных уже сформирован классом listview
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title=context['post'])
        return dict(list(context.items()) + list(c_def.items()))


#  def show_post(request, post_slug):
#     post = get_object_or_404(Eat, slug=post_slug)
#     context = {
#         'title': post.title,
#         'menu': menu,
#         'post': post,
#     }
#  напитки
#     return render(request, 'app1/post.html', context=context)


# класс, отвечающий за показ категории
class EatCategory(DataMixin, ListView):
    model = Eat
    template_name = 'app1/index.html'
    context_object_name = 'posts'
    #  чтобы когда вводят несуществующую категорию в url и не давало ошибку в get_context_data
    allow_empty = False

    def get_queryset(self):
        # ['category_slug] мы берем из маршрута absolute_url , category__slug означает что мы обращаемся к полю slug таблицы сategory, связаной с текущей записью
        # print(Eat.objects.filter(category__slug='pizza', is_existed=True))
        # доказывает, что берется из absolute_url в models в Category
        # print(self.kwargs)
        # self.kwargs вместо передаваемого параметра вместе с request в функции, если не класс
        return Eat.objects.filter(category__slug=self.kwargs['category_slug'], is_existed=True)

    def get_context_data(self, *, object_list=None, **kwargs):
        # этот контекст данных уже сформирован классом listview
        context = super().get_context_data(**kwargs)

        # этот запрос является дублем
        # c_def = self.get_user_context(title="Категория - " + str(context['posts'][0].category),
        #                               cat_selected=context['posts'][0].category_id)

        # облегчим систему
        c = Category.objects.get(slug=self.kwargs['category_slug'])
        c_def = self.get_user_context(title="Категория - " + str(c.name),
                                      cat_selected=c.pk)
        return dict(list(context.items()) + list(c_def.items()))


# def show_category(request, category_slug):
#     # Здесь я профильтровал записи по слагу и потом вытащил pk из совпадающей записи
#     category_id = Category.objects.get(slug=category_slug).pk
#
#     posts = Eat.objects.filter(category_id=category_id)
#     # второй способ без category_id
#     # posts = Eat.objects.filter(category__slug=category_slug)
#     if len(posts) == 0:
#         return HttpResponseNotFound('<h1>Страница не найдена</h1>')
#     context = {
#         'title': "Позиции",
#         # 'menu': menu, уже не надо, есть тэг
#         'posts': posts,
#         'category_slug': category_slug,
#         'cat_selected': category_id
#
#     }
#     return render(request, 'app1/index.html', context=context)


class RegisterUser(DataMixin, CreateView):
    form_class = RegisterUserForm
    template_name = 'app1/register.html'
    # перенаправление при успешной регистрации
    success_url = reverse_lazy('login')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Регистрация")
        return dict(list(context.items()) + list(c_def.items()))

    # метод вызывается при успешной регистрации
    def form_valid(self, form):
        # сохраняем пользователя в базу данных
        user = form.save()
        # и после этого сразу авторизовываем
        # импортируем функцию login для авторизации
        login(self.request, user)
        # и после этого его направляем на home
        return redirect('home')
class LoginUser(DataMixin, LoginView):
    form_class = LoginUserForm  # наша форма вместо, стандартной AuthenticationForm
    template_name = 'app1/login.html'
    # перенаправление при успешной регистрации
    success_url = reverse_lazy('login')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Авторизация")
        return dict(list(context.items()) + list(c_def.items()))

    def get_success_url(self):
        return reverse_lazy('home')


# def login(request):
#     return HttpResponse("Авторизация")


# нам здесь не нужен класс представления, потому что функционал очень простой
def logout_user(request):
    # стандартная django функция logout, чтобы пользователь мог выйти из авторизации
    logout(request)
    # перенаправление на login вкладку (маршрут)
    return redirect('login')


# def contact(request):
#     return HttpResponse("Обратная связь")


# FormView не привязана к бд, поэтому не будет с ней работать
class ContactFormView(DataMixin, FormView):
    form_class = ContactForm
    template_name = 'app1/contact.html'
    # перенаправление при успешной регистрации
    success_url = reverse_lazy('home')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Обратная связь")
        return dict(list(context.items()) + list(c_def.items()))

    # метод вызывается, если пользователь успешно заполнил все поля контактной формы
    def form_valid(self, form):
        # здесь в виде словаря выводятся данные, которые мы заполнили на сайте
        print(form.cleaned_data)
        # и после этого его направляем на home
        return redirect('home')