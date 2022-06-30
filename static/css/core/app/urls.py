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
from django.urls import path

from . import views

# import threading


urlpatterns = [
    path('dashboard/', views.appDashboard, name='appDashboard'),
    path('strategy/', views.appStrategy, name='appStrategy'),
    path('strategy/<int:strategy_id>', views.appStrategyId, name='appStrategyId'),
    path('strategy/<int:strategy_id>/switch', views.appStrategySwitchStatus, name='appStrategySwitchStatus'),
    path('telegram-alert/switch', views.appTelegramAlertSwitch, name='appTelegramAlertSwitch'),
    path('strategy/follow/<str:typer>/<int:strategy_id>/', views.appStrategyFollowId, name='appStrategyFollowId'),
    path('settings/', views.appSettings, name='appSettings'),
    path('settings/<int:id_sub>/set-percent/', views.appSetPercent, name='appSetPercent'),
    path('settings/removetg/<int:tg_id>', views.appRemoveTg, name='appRemoveTg'),
    path('balance/<str:_type>', views.appBalance, name='appBalance'),
    path('transaction/<str:id>/set-status/<str:status>', views.appTransactionsSetStatus, name='appTransactionsSetStatus'),
    path('accounts/', views.appAccounts, name='appAccounts'),
    path('accounts/<int:id_key>/switch', views.appAccountsSwitchStatus, name='appAccountsSwitchStatus'),
    path('accounts/remove/<int:id_key>', views.appAccountsRemoveKey, name='appAccountsRemoveKey'),
    path('api-keys/', views.appAPIKeys, name='appAPIKeys'),
    path('api-tg/', views.appTGKeys, name='appTGKeys'),
    path('2FA/', views.app2FA, name='app2FA'),
    path('pools/', views.appPools, name='appPools'),
    path('pool/<int:pool_id>', views.appPool, name='appPool'),
    # path('beginning-payment/', views.beginningPayment, name='beginningPayment'),
    path('payment/<str:_status>', views.appPayment, name='appPayment'),

    # Тест (распределения денег при оплате)
    path('payment/', views.payments, name='payment'),
    path('tg/', views.tg, name='tg'),
    # Тест (Запись логов)
    path('recording_logs/', views.recordingLogs, name='recording_logs'),
    path('referral/', views.appReferral, name='appReferral'),
]
