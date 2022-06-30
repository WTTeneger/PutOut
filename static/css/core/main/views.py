import random
# from datetime import datetime, timedelta

from django import forms
from django.conf import settings
from django.contrib.auth import login, logout
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.core.validators import validate_email
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.template.loader import render_to_string
from django.utils import translation
from django.utils.translation import gettext_lazy as _
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view

from ..api.views import createUserData
from ..app.thirdparty_functions import distribution_of_money, recording_logs
from ..utils.utils import __check_auth, __check_registers
from .forms import CheckVerificationForm, SignInForm, SignUpForm
from .models import *


def index(request):
    return render(request, 'main/index.html', {'languages': settings.LANGUAGES})


def referral(request, referral_key=''):
    request.session['referral_key'] = referral_key
    return redirect('index')


def signIn(request):
    """Авторизация пользователя"""
    if request.user.is_authenticated:
        return redirect('appDashboard')
    if request.method == 'POST':
        form = SignInForm(request.POST)
        if form.is_valid():
            auth_user = User.objects.get(username=form.cleaned_data['email'])
            # Проверка на двухФакторку
            ver_user = UserData.objects.filter(mail=form.cleaned_data['email'])
            if ver_user.exists() and ver_user.first().TwoFA and ver_user.first().TwoFA.verificated:
                request.session['verificated_data'] = {'mail': form.cleaned_data['email'],
                                                       'password': form.cleaned_data['password']}
                return redirect('verificated')
            login(request, auth_user)
            return redirect('appDashboard')
    else:
        form = SignInForm()
    return render(request, 'main/sign-in.html', {'form': form})


def verificated(request):
    """Двойная верификация пользователя"""
    if request.method == 'POST':
        form = CheckVerificationForm(request.POST, client=request.session['verificated_data'])
        if form.is_valid():
            print('user', form.user)
            login(request, form.user)
            return redirect('appDashboard')
    else:
        if 'verificated_data' in request.session:
            dt = request.session['verificated_data']
        else:
            return redirect('sign-in')
    if request.method == 'GET':
        form = CheckVerificationForm(client='')
    # print(form)
    return render(request, 'main/TwoFA_verificated.html', {'form': form})


@api_view(['POST'])
@csrf_exempt  # Декоратор проверки
def my_send_mail(request):
    v_code = random.randint(100_000, 999_999)
    # TODO заменить везде на request.POST
    if request.GET.get('email'):
        # TODO Доделать проверку на то есть ли уже заргенная почта
        try:
            validate_email(request.GET.get('email', ''))
            VE = VerifyEmail.objects.filter(email=request.GET.get('email'))
            if VE:
                VE[0].code = v_code
                VE[0].save()
            else:
                VerifyEmail.objects.create(email=request.GET.get('email'), code=v_code)
            send_mail(
                auth_user=settings.EMAIL_HOST_USER,
                auth_password=settings.EMAIL_HOST_PASSWORD,
                subject='LuckyTrader - {}'.format(_('Код Верификации')),
                message='test message',
                html_message=render_to_string('main/email.html', {
                    'code': v_code
                }),
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[request.GET.get('email')]
            )
        except forms.ValidationError:
            pass
    response = HttpResponse('qwe')
    response.status_code = 200
    return response


def test(request):
    # import uuid
    # print(uuid.uuid4())

    # datetime.timezone(offset, name='МСК')
    # now = timezone.now() + timedelta(hours=3)
    # f = VerifyEmail.objects.filter(
    #     date__lt=(now - timedelta(minutes=15))
    # )  # .filter(date__year='2022')
    # .filter(date__range=["2022-05-17 21:07:08.720407", datetime.now()])#all().first()
    # g = datetime.strptime('2022-05-17 21:07:08.720407+00:00', '%Y-%m-%d %H:%M:%S.%f')
    return HttpResponse('ok')


def signUp(request):
    """Регистрация пользователя"""
    if request.user.is_authenticated:
        return redirect('appDashboard')

    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            data = {
                'email': form.cleaned_data['email'],
                'password1': form.cleaned_data['password']
            }
            if 'referral_key' in request.session:
                data['referral_key'] = str(request.session.get('referral_key'))
            new_user = createUserData(data)
            login(request, new_user.login)
            return redirect('appDashboard')
    else:
        form = SignUpForm()
    return render(request, 'main/sign-up.html', {'form': form})


def create_data_header(data=None, request=None):
    user = ''
    return_data = {}
    if data:
        return_data = return_data | data
    return return_data


@api_view(['GET'])
def main(request):
    # createUserData({'email': 'am11111al@11ka', 'password1': 'pass', 'referral_key': 'csq5R2lV'})
    distribution_of_money(UserData.objects.get(id=18), 150)
    recording_logs(UserData.objects.get(id=18), 'Пополнил баланс', 150)
    return HttpResponse('result')


# @api_view(['GET'])  # TODO сменить
# @__check_auth  # Декоратор проверки авторизации
# @__check_registers  # Декоратор проверки оплаты входа


def logoutUser(request, data_auth=None):
    logout(request)
    return redirect('sign-in')


@api_view(['GET'])
def addChangeLanguage(request, lang='ru'):
    # Смена языка
    next = request.META.get('HTTP_REFERER')
    next = next.replace(f'/{request.LANGUAGE_CODE}', f'/{lang}')
    translation.activate(lang)
    return redirect(next)
#
# def coursesPage(request):
#     # if request.user.is_authenticated:
#     #     return redirect('/a/')
#     courses = Courses.objects.all()
#     data = {'courses': courses}
#     data = create_data_header(data)
#     return render(request=request, context=data, template_name='main/courses.html')

#
# def paymentPage(request):
#     # if request.user.is_authenticated:
#     #     return redirect('/a/')
#     courses = Courses.objects.all()
#     data = {'courses': courses}
#     data = create_data_header(data)
#     return render(request=request, context=data, template_name='main/payment.html')


# translation.activate('ru') Код перевода локали
