from django.contrib.auth.forms import UserCreationForm

from users.models import User


class UserRegisterForm(UserCreationForm):
    usable_password = None

    class Meta:
        model = User
        fields = ('email', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['email'].widget.attrs.update({
            'placeholder': 'Укажите ваш email',
            'class': 'form-control'
        })

        self.fields['password1'].widget.attrs.update({
            'placeholder': 'Создайте пароль',
            'class': 'form-control'
        })

        self.fields['password2'].widget.attrs.update({
            'placeholder': 'Повторите пароль',
            'class': 'form-control'
        })
