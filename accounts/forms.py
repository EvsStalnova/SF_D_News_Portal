from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from allauth.account.forms import SignupForm
from django.contrib.auth.models import Group


class SignUpForm(UserCreationForm):
    email = forms.EmailField(label="Email")
    first_name = forms.CharField(label="Имя")
    last_name = forms.CharField(label="Фамилия")


    class Meta:
        model = User
        fields = (
            "username",
            "first_name",
            "last_name",
            "email",
            "password1",
            "password2",
        )


class CustomSignUpForm(SignupForm):
    def save(self, request):
        user = super().save(request)

        subject = 'Добро пожаловать на наш новостной портал!'
        text = f'{user.username}, Вы успешно зарегистрировались на нашем новостном портале!'
        html = (
            f'<b>{user.username}</b>, Вы успешно зарегистрировались на '
            f'<a href="http://127.0.0.1:8000/post">нашем новостном портале!</a>'
        )
        msg = EmailMultiAlternatives(
            subject=subject, body=text, from_email=settings.DEFAULT_FROM_EMAIL, to=[user.email]
        )
        msg.attach_alternative(html, "text/html")
        msg.send()
        return user