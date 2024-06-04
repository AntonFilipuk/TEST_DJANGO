from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from captcha.fields import CaptchaField
from .models import *


class AddPostForm(forms.ModelForm):
    ## widget и attrs можно прописать класс, чтобы потом офорить его уже не в html, а напрямую в css
    # title = forms.CharField(max_length=255, label='Название',widget=forms.TextInput(attrs={'class': 'form-input'}))
    # slug = forms.SlugField(max_length=255, label='URL')
    # description = forms.CharField(widget=forms.Textarea(attrs={'cols': 60, 'rows': 10}), label='Описание')
    # is_existed = forms.BooleanField(label="Подтверждение",required=False, initial=True) #initial=True - чекбокс делает отмеченным
    # category = forms.ModelChoiceField(queryset=Category.objects.all(), label='Категории', empty_label='Категория не выбрана')

    # прописываем конструктор, чтобы отображался текст в пустом поле выбора категории
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['category'].empty_label = "Категория не выбрана"

    class Meta:
        model = Eat  # связь формы с моделью EAT
        fields = ['title', 'slug', 'description', 'photo', 'is_existed',
                  'category']  # какие поля нужно отобразить, кроме тех, что заполняются автоматически
        # здесь точесно настраиваем каждое поле формы
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-input'}),
            'content': forms.Textarea(attrs={'cols': 60, 'rows': 10}),
        }

    # метод, который будет отвечать за пользовательскую валидацию clean_<название столбца>
    # валидатор для тайтла конкр
    def clean_title(self):
        title = self.cleaned_data['title']
        if len(title) > 100:
            raise ValidationError('Длина превышает 100 символов')
        # Иначе просто возвращается заголовок
        return title


class RegisterUserForm(UserCreationForm):
    # переопределяем поля, потому что на них не работают стили
    username = forms.CharField(label='Логин', widget=forms.TextInput(attrs={'class': 'form-input'}))
    email = forms.EmailField(label=' Email', widget=forms.EmailInput(attrs={'class': 'form-input'}))
    password1 = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-input'}))
    password2 = forms.CharField(label='Повторите пароль', widget=forms.PasswordInput(attrs={'class': 'form-input'}))

    # расширяем класс UserCreationForm, то есть расширяем регистрацию
    class Meta:
        # работает с таблицей auth_user в SQL
        model = User
        # поля, которые будут отображаться
        fields = ('username', 'email', 'password1', 'password2')

        # оформление для каждого из полей
        # widgets = {
        #     'username': forms.TextInput(attrs={'class': 'form-input'}),
        #     'password1': forms.PasswordInput(attrs={'class': 'form-input'}),
        #     'password2': forms.PasswordInput(attrs={'class': 'form-input'}),
        #  }


class LoginUserForm(AuthenticationForm):
    username = forms.CharField(label='Логин', widget=forms.TextInput(attrs={'class': 'form-input'}))
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-input'}))


# наследуется от Form - это общий класс формы и три поля далее идет
class ContactForm(forms.Form):
    name = forms.CharField(label='Имя', max_length=255)
    email = forms.EmailField(label=' Email')
    content = forms.CharField(widget=forms.Textarea(attrs={'cols': 60, 'rows': 10}))
    captcha = CaptchaField()
