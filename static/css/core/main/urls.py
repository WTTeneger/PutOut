"""lt URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.urls import path
from .forms import UserPasswordResetForm, UserSetPasswordForm
from . import views
from django.contrib.auth import views as auth_views
from django.urls import reverse_lazy

urlpatterns = [
    path('', views.index, name='index'),
    path('referral/<referral_key>', views.referral, name='referral'),
    path('result/', views.main),

    # Авторизация, деавторизация
    path('sign-out/', views.logoutUser, name='sign-out'),

    path('password_reset/',
         auth_views.PasswordResetView.as_view(
             from_email=settings.EMAIL_HOST_USER,
             template_name='main/password_reset_form.html',
             form_class=UserPasswordResetForm,
             html_email_template_name='main/password_reset_email.html'
         ),
         name='password_reset'),
    path('password_reset/done/',
         auth_views.PasswordResetDoneView.as_view(template_name='main/password_reset_done.html'),
         name='password_reset_done'),
    path('reset/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(template_name='main/password_reset_confirm.html',
                                                     form_class=UserSetPasswordForm,
                                                     success_url=reverse_lazy('sign-in')),
         name='password_reset_confirm'),
    # path('reset/done/',
    #      auth_views.PasswordResetCompleteView.as_view(template_name='main/password_reset_complete.html'),
    #      name='password_reset_complete'),
    # Страница курсов
    # path('courses/', views.coursesPage),
    # path('payment/', views.paymentPage),
    path('my_send_mail/', views.my_send_mail, name='my_send_mail'),
    path('sign-in/', views.signIn, name='sign-in'),
    path('sign-up/', views.signUp, name='sign-up'),
    path('change-language/<str:lang>', views.addChangeLanguage, name='addChangeLanguage'),

    path('verificated/', views.verificated, name='verificated'),
    path('test/', views.test, name='__'),
]

# handler404 = 'core.main.views.handler404'
