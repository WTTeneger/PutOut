
import unicodedata
from datetime import timedelta

from django import forms
from django.conf import settings
from django.contrib.auth import (authenticate, get_user_model,
                                 password_validation)
from django.contrib.auth.forms import PasswordResetForm, SetPasswordForm
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.core.exceptions import ValidationError
from django.core.mail import EmailMultiAlternatives
from django.template import loader
from django.utils import timezone
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.utils.translation import gettext_lazy as _
from password_strength import PasswordStats
from services.twofactorauth import TwoFactorAuth

from .models import VerifyEmail, UserData

UserModel = get_user_model()
# from django.core.validators import validate_email
# from ..utils.utils import check_correct_password


def _unicode_ci_compare(s1, s2):
    """
    Perform case-insensitive comparison of two identifiers, using the
    recommended algorithm from Unicode Technical Report 36, section
    2.11.2(B)(2).
    """
    return (
        unicodedata.normalize("NFKC", s1).casefold()
        == unicodedata.normalize("NFKC", s2).casefold()
    )


class UserPasswordResetForm(PasswordResetForm):
    def __init__(self, *args, **kwargs):
        super(UserPasswordResetForm, self).__init__(*args, **kwargs)

    email = forms.EmailField(
        label='',
        widget=forms.EmailInput(attrs={
            'placeholder': _('Email'),
            'class': 'input-text-default',
            'type': 'text',
            'id': 'user-login'
        }))

    def send_mail(
        self,
        subject_template_name,
        email_template_name,
        context,
        from_email,
        to_email,
        html_email_template_name=None,
    ):
        """
        Send a django.core.mail.EmailMultiAlternatives to `to_email`.
        """
        subject = loader.render_to_string(subject_template_name, context)
        # Email subject *must not* contain newlines
        subject = "".join(subject.splitlines())
        body = loader.render_to_string(email_template_name, context)

        email_message = EmailMultiAlternatives(subject, body, from_email, [to_email])
        if html_email_template_name is not None:
            html_email = loader.render_to_string(html_email_template_name, context)
            email_message.attach_alternative(html_email, "text/html")

        email_message.send()

    def get_users(self, email):
        """Given an email, return matching user(s) who should receive a reset.

        This allows subclasses to more easily customize the default policies
        that prevent inactive users and users with unusable passwords from
        resetting their password.
        """
        # email_field_name = UserModel.get_email_field_name()
        active_users = UserModel.objects.filter(
            **{
                "username__iexact": email,
                "is_active": True,
            }
        )
        u = (
            u
            for u in active_users
            if u.has_usable_password()
            and _unicode_ci_compare(email, getattr(u, 'username'))
        )
        # print([u for u in active_users if u.has_usable_password()])
        # print([u for u in active_users if _unicode_ci_compare(email, getattr(u, 'username'))])
        print([u
               for u in active_users
               if u.has_usable_password()
               and _unicode_ci_compare(email, getattr(u, 'username'))])
        return u

    def save(
        self,
        domain_override=None,
        subject_template_name="registration/password_reset_subject.txt",
        email_template_name="registration/password_reset_email.html",
        use_https=False,
        token_generator=default_token_generator,
        from_email=None,
        request=None,
        html_email_template_name=None,
        extra_email_context=None,
    ):
        """
        Generate a one-use only link for resetting password and send it to the
        user.
        """
        email = self.cleaned_data["email"]
        if not domain_override:
            current_site = get_current_site(request)
            site_name = current_site.name
            domain = current_site.domain
        else:
            site_name = domain = domain_override
        for user in self.get_users(email):
            user_email = getattr(user, 'username')
            context = {
                "email": user_email,
                "domain": domain,
                "site_name": site_name,
                "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                "user": user,
                "token": token_generator.make_token(user),
                "protocol": "https" if use_https else "http",
                **(extra_email_context or {}),
            }
            self.send_mail(
                subject_template_name,
                email_template_name,
                context,
                from_email,
                user_email,
                html_email_template_name=html_email_template_name,
            )


class UserSetPasswordForm(SetPasswordForm):
    new_password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'placeholder': _('Новый пароль'),
            'class': 'input-text-default',
            'type': 'text',
            'id': 'user-login'
        }),
        strip=False,
        help_text=password_validation.password_validators_help_text_html(),
    )
    new_password2 = forms.CharField(
        strip=False,
        widget=forms.PasswordInput(attrs={
            'placeholder': _('Повторите новый пароль'),
            'class': 'input-text-default',
            'type': 'text',
            'id': 'user-login'
        }),
    )


class CheckVerificationForm(forms.Form):
    code_from_2FA = forms.CharField(
        max_length=6,
        widget=forms.TextInput(
            attrs={
                'placeholder': _('6-ти значный код из приложения'),
                'class': 'input-text-default',
                'type': 'text',
                'name': 'name-integration',
                'id': 'name-integration'
            }
        )
    )

    def __init__(self, *args, **kwargs):
        client = kwargs.pop('client', None)
        self.client = client
        super(CheckVerificationForm, self).__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super().clean()

        print('self')
        print(self.client)
        if 'mail' not in self.client or 'password' not in self.client:
            raise ValidationError(_('Нет данных'))
        user = authenticate(
            username=self.client['mail'],
            password=self.client['password']
        )
        self.user = user

        u = UserData.objects.filter(login=user)
        # Проверяем существование пользователя
        if not user and not u:
            raise ValidationError(_('Неправильный логин или пароль'))

        u = u[0]

        if 'code_from_2FA' not in cleaned_data:
            raise ValidationError(_('Вы не отправили код'))
        print(u.TwoFA.code)
        valid = TwoFactorAuth().validate(secret=u.TwoFA.code, code=cleaned_data['code_from_2FA'])
        if valid == 'False':
            raise ValidationError(_('Не верный код'))


def check_correct_password(password):
    """Проверка пароля на сложность"""
    # Если не достаточно разнообразный
    if PasswordStats(password).strength() < settings.PASSWORD_STRENGTH:
        raise ValidationError(_('Придумайте более сложный пароль'))
    # Если неправильный пароль
    elif settings.POLICY.test(password):
        raise ValidationError(
            _('Пароль должен быть длиннее 8 символов и содержать по крайней мере одну заглавную букву, цифру и специальный символ'))


class SignInForm(forms.Form):
    """Авторизация"""
    email = forms.CharField(
        max_length=250,
        widget=forms.TextInput(
            attrs={
                'placeholder': _('Email'),
                'class': 'input-text-default',
                'type': 'text',
                'id': 'user-login'
            }
        )
    )
    password = forms.CharField(
        max_length=250,
        # widget=forms.PasswordInput,
        widget=forms.TextInput(
            attrs={
                'placeholder': _('Password'),
                'class': 'input-text-default',
                'type': 'password',
                'id': 'user-pass',
                'data-input-pass': '1',
            }
        )
    )

    def clean(self):
        # print(super().clean())
        cleaned_data = super().clean()
        # print(cleaned_data)
        user = authenticate(
            username=cleaned_data['email'],
            password=cleaned_data['password']
        )
        # Проверяем существование пользователя
        if not user:
            raise ValidationError(_('Неправильный логин или пароль'))


class SignUpForm(forms.Form):
    """Регистрация"""
    email = forms.EmailField(
        max_length=250,
        widget=forms.TextInput(
            attrs={
                'placeholder': _('Email'),
                'class': 'input-text-default',
                'id': 'user-login',
                'name': 'User Login'
            }
        )
    )
    code = forms.CharField(
        max_length=6,
        widget=forms.TextInput(
            attrs={
                'placeholder': _('Code'),
                'class': 'input-text-default',
                'id': 'user-code',
                'name': 'User Code'
            }
        )
    )
    password = forms.CharField(
        max_length=250,
        widget=forms.TextInput(
            attrs={
                'placeholder': _('Password'),
                'class': 'input-text-default',
                'type': 'password',
                'id': 'user-pass',
                'name': 'User Password',
                'data-input-pass': "1",
            }
        )
    )
    confirm_password = forms.CharField(
        max_length=250,
        widget=forms.TextInput(
            attrs={
                'placeholder': _('Confirm Password'),
                'class': 'input-text-default',
                'type': 'password',
                'id': 'user-pass-repeat',
                'data-input-pass': "2",
            }
        )
    )

    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get('email')
        code = cleaned_data.get('code')
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')
        v_user = VerifyEmail.objects.filter(email=email, code=code).only('code')
        # Если имя занято
        if User.objects.filter(username=email).exists():
            raise ValidationError(_('Логин занят'))
        # Если кода нет(очистили уже)
        elif not v_user.exists():
            raise ValidationError(_('Срок действия кода истек, пожалуйста, повторите проверку'))
        # Проверка совпадения кода
        elif not v_user:
            raise ValidationError(_('Неправильный код'))
        # Если повторный пароль не совпадает
        elif password != confirm_password:
            raise ValidationError(_('Пароли не совпадают'))
        # Отправляем пароль на проверку
        check_correct_password(password)
        # Удаляем запись
        v_user.delete()
        # Удаляем все записи старше 15 минут TODO доделать
        VerifyEmail.objects.filter(
            date__lt=(
                (
                    timezone.now() + timedelta(hours=3) - timedelta(minutes=15)
                )
            )
        ).delete()
