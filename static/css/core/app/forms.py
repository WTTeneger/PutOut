import datetime

from django import forms
from django.conf import settings
from django.contrib.auth import authenticate
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
# from django.core.validators import validate_email
# from ..utils.utils import check_correct_password
from password_strength import PasswordStats

from binance_api.binance_a import Binance
from core.app.thirdparty_functions import take_money_from_user
from core.main.models import APIKeys, TelegramAccount, Transactions, SiteConfiguration, PoolUsers
# from app import settings
from services.twofactorauth import TwoFactorAuth
from services.payment import Payment
from tg_bot import send_message


def check_correct_password(password):
    """Проверка пароля на сложность"""
    # Если не достаточно разнообразный
    if PasswordStats(password).strength() < settings.PASSWORD_STRENGTH:
        raise ValidationError(_('Придумайте более сложный пароль'))
    # Если неправильный пароль
    elif settings.POLICY.test(password):
        raise ValidationError(
            _('Пароль должен быть длиннее 8 символов и содержать по крайней мере одну заглавную букву, цифру и специальный символ'))


class APIKeysForm(forms.Form):
    """Авторизация"""
    CHOICES = (('Binance', 'Binance'), ('ByByt', 'ByBit'),)
    # select = forms.CharField(widget=forms.Select(choices=CHOICES))
    attrs = {
        'placeholder': _('Биржа'),
        'class': 'custom-select__select-default',
        'type': 'select',
        'name': 'select',
        'id': 'select-1'
    }
    place = forms.ChoiceField(widget=forms.Select(attrs=attrs), choices=CHOICES)

    name_integration = forms.CharField(
        max_length=250,
        widget=forms.TextInput(
            attrs={
                'placeholder': _('Имя интеграции'),
                'class': 'input-text-default',
                'type': 'text',
                'name': 'name-integration',
                'id': 'name-integration'
            }
        )
    )

    public_key = forms.CharField(
        max_length=250,
        # widget=forms.PasswordInput,
        widget=forms.TextInput(
            attrs={
                'placeholder': _('Публичный ключ'),
                'class': 'input-text-default',
                'type': 'password',
                'name': 'api-key',
                'id': 'api-key',
                'data-input-pass': '10',
            }
        )
    )
    private_key = forms.CharField(
        max_length=250,
        # widget=forms.PasswordInput,
        widget=forms.TextInput(
            attrs={
                'placeholder': _('Приватный ключ'),
                'class': 'input-text-default',
                'type': 'password',
                'name': 'api-key',
                'id': 'api-key',
                'data-input-pass': '11',
            }
        )
    )

    def clean(self):
        cleaned_data = super().clean()
        bot = Binance(
            API_KEY=cleaned_data['public_key'],
            API_SECRET=cleaned_data['private_key']
        )
        acc = {}
        try:
            acc = bot.account()
        except:
            acc['code'] = 'ERRORs'
        if not 'code' in acc:
            if APIKeys.objects.filter(place=cleaned_data['place'],
                                      key_public=cleaned_data['public_key'],
                                      key_private=cleaned_data['private_key']):
                raise ValidationError(_('Не удалось привязать аккаунт. Эти данные ключи уже используются'))

            else:
                new_api_keys = APIKeys()
                new_api_keys.place = cleaned_data['place']
                new_api_keys.title = cleaned_data['name_integration']
                new_api_keys.key_public = cleaned_data['public_key']
                new_api_keys.key_private = cleaned_data['private_key']
                new_api_keys.save()
        else:
            raise ValidationError(_('Не удалось привязать аккаунт. Перепроверьте данные и введите их еще раз.'))


class TGKeysForm(forms.Form):
    """Авторизация"""
    # select = forms.CharField(widget=forms.Select(choices=CHOICES))

    name_integration = forms.CharField(
        max_length=20,
        widget=forms.TextInput(
            attrs={
                'placeholder': _('Имя интеграции'),
                'class': 'input-text-default',
                'type': 'text',
                'name': 'name-integration',
                'id': 'name-integration'
            }
        )
    )

    tg_key = forms.CharField(
        max_length=250,
        # widget=forms.PasswordInput,
        widget=forms.TextInput(
            attrs={
                'placeholder': _('TG ключ'),
                'class': 'input-text-default',
                'type': 'text',
            }
        )
    )

    def clean(self):
        cleaned_data = super().clean()
        acc = {}
        try:
            pass
        except:
            acc['code'] = 'ERRORs'
        if not 'code' in acc:
            if TelegramAccount.objects.filter(tg_token=cleaned_data['tg_key']):
                raise ValidationError(_('Не удалось привязать аккаунт. Этот ключ уже используется'))

            else:
                new_api_keys = TelegramAccount()
                a = send_message([cleaned_data['tg_key']], (f'Ваш телеграмм аккаунт проверен'))
                if not a:
                    raise ValidationError(_('Не удалось привязать аккаунт. Данный тг аккаунт не подключен в боте.'))
                new_api_keys.title = cleaned_data['name_integration']
                new_api_keys.tg_token = cleaned_data['tg_key']
                new_api_keys.save()
        else:
            raise ValidationError(_('Не удалось привязать аккаунт. Перепроверьте данные и введите их еще раз.'))


class TwoFactorAuthForm(forms.Form):
    """Двух факторная утентификация"""
    # select = forms.CharField(widget=forms.Select(choices=CHOICES))

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
        # Принимаем юзера из views
        client = kwargs.pop('client', None)
        self.client = client
        super(TwoFactorAuthForm, self).__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super().clean()
        acc = {}
        if self.client.TwoFA:
            secret = self.client.TwoFA.code
            qr = TwoFactorAuth()
            vl = qr.validate(secret=secret, code=cleaned_data['code_from_2FA'])
            if vl == 'True':
                self.client.TwoFA.verificated = True
                self.client.TwoFA.save()
            else:
                raise ValidationError(_('Не удалось привязать аккаунт. Перепроверьте ключ'))
        else:
            raise ValidationError(_('Не удалось привязать аккаунт. Перезапуститите страницу и исользуйте qr заного'))


class PasswordChange(forms.Form):
    """Смена пароля"""
    old_password = forms.CharField(
        max_length=250,
        min_length=8,
        widget=forms.TextInput(
            attrs={
                'placeholder': _('Текущий пароль'),
                'class': 'input-text-default',
                'type': 'password',
                # 'name': 'password-1',
                'id': 'user-pass-1',
                'data-input-pass': 1
            }
        )
    )
    new_password = forms.CharField(
        max_length=250,
        min_length=8,
        widget=forms.TextInput(
            attrs={
                'placeholder': _('Новый пароль'),
                'class': 'input-text-default',
                'type': 'password',
                # 'name': 'password-2',
                'id': 'user-pass-2',
                'data-input-pass': 2
            }
        )
    )
    confirm_new_password = forms.CharField(
        max_length=250,
        min_length=8,
        widget=forms.TextInput(
            attrs={
                'placeholder': _('Подтвердите новый пароль'),
                'class': 'input-text-default',
                'type': 'password',
                # 'name': 'password-3',
                'id': 'user-pass-3',
                'data-input-pass': 3
            }
        )
    )

    def __init__(self, *args, **kwargs):
        # Принимаем юзера из views
        user_id = kwargs.pop('user_id', None)
        self.user_id = user_id
        super(PasswordChange, self).__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super().clean()
        user = authenticate(
            username=self.user_id,
            password=cleaned_data['old_password']
        )
        # Проверяем существование пользователя
        if not user:
            raise ValidationError(_('Неправильный логин или пароль'))
        if cleaned_data['new_password'] != cleaned_data['confirm_new_password']:
            raise ValidationError(_('Пароли не совпадают'))
        # Отправляем пароль на проверку
        check_correct_password(cleaned_data['new_password'])


class UserNameChange(forms.Form):
    login = forms.CharField(
        max_length=250,
        widget=forms.TextInput(
            attrs={
                'placeholder': _('Имя пользователя'),
                'class': 'input-text-default',
                'name': 'change-username',
                'id': 's1',
                'type': 'text',
            }
        )
    )


class NewTransfer(forms.Form):
    CHOICES_COIN = (
        ('USDT', _('USDT (TRC20)')),
    )
    CHOICES_PLACE = (
        ('Crypto', _('Криптой')),
        ('Card', _('Картой')),
    )
    CHOICES_PLACE = CHOICES_PLACE if settings.PAY_CARD else (('Crypto', _('Криптой')),)
    pc = settings.PAY_CARD
    # select = forms.CharField(widget=forms.Select(choices=CHOICES))
    attrs_place = {
        'placeholder': _('Метод пополнения'),
        'class': 'custom-select__select-default',
        'type': 'select',
        'name': 'select',
        'm-balance-change': 'area',
        'id': 'm-balance-1',
        'onchange': 'set_payment_method(this)',
        'required': 'false'
    }
    attrs_coin = {
        'placeholder': _('Монета'),
        'class': 'custom-select__select-default',
        'type': 'select',
        'name': 'select',
        'm-balance-change': 'coin',
        'id': 'm-balance-2',
        'onchange': 'set_payment_method(this)',
        'required': 'false'
    }
    place = forms.ChoiceField(widget=forms.Select(attrs=attrs_place), choices=CHOICES_PLACE)
    coin = forms.ChoiceField(widget=forms.Select(attrs=attrs_coin), choices=CHOICES_COIN)

    address = forms.CharField(
        min_length=1,
        max_length=100,
        required=False,
        widget=forms.TextInput(
            attrs={
                'placeholder': _('Tkjw...VWQGF'),
                'class': 'u-input input-el__area',
                'type': 'text',
                'name': "m-balance-3",
                'id': 'm-balance-3',
            }
        )
    )
    total = forms.IntegerField(
        min_value=1,
        widget=forms.TextInput(
            attrs={
                'placeholder': '0',
                'class': 'u-input input-el__area',
                'type': 'text',
                'name': "m-balance-4",
                'id': 'm-balance-4'
            }
        )
    )

    def __init__(self, *args, **kwargs):
        # Принимаем юзера из views
        user = kwargs.pop('ud', None)
        self.user = user
        self.cd = None
        super(NewTransfer, self).__init__(*args, **kwargs)

    def create_transfer(self):
        nt = Transactions()
        nt.from_user = self.user
        nt.total = int(self.cd['total'])
        nt.wallet = '' if not 'address' in self.cd else self.cd['address']
        nt.type = nt.ORDER_TYPE[0][0]
        nt.type_pay = self.cd['place']
        nt.status = nt.ORDER_STATUS[0][0]
        nt.save()
        if self.cd['place'] == "Card":
            url = Payment().create_url(order_id=f"{self.user.id}_{nt.uuid}", total=int(self.cd['total'])*50,
                                       customer_phone='79999999999', customer_email=self.user.mail, demo_mode=False)
            nt.payment_url = url
            nt.save()
    def set_status_active(self):
        if self.cd['total'] >= SiteConfiguration.objects.first().entry_fee:
            self.user.verified = True
            self.user.free_sub = True
            self.user.save()

    def clean(self):
        cd = super().clean()
        self.cd = cd
        print('cd', cd)
        if 'total' in cd:
            if cd['total'] > 0:
                if cd['place'] == 'Card' and int(cd['total']) > 0:
                    self.create_transfer()
                elif cd['place'] == 'Crypto' and int(cd['total']) > 0 and cd['coin']:
                    self.create_transfer()
                else:
                    raise ValidationError(_('Некоторые поля не заполнены'))
            else:
                raise ValidationError(_('Сумма пополнение должна быть больше или ровна 0'))
        else:
            raise ValidationError(_('Некоторые поля не заполнены'))


class Withdrawal(forms.Form):
    CHOICES_COIN = (
        ('USDT', _('USDT (TRC20)')),
    )
    CHOICES_PLACE = (
        ('Crypto', _('Криптой')),
    )
    pc = settings.PAY_CARD
    # select = forms.CharField(widget=forms.Select(choices=CHOICES))
    attrs_place = {
        'placeholder': _('Метод вывода'),
        'class': 'custom-select__select-default',
        'type': 'select',
        'name': 'select',
        'm-balance-change': 'area',
        'id': 'm-balance-1',
        'onchange': 'set_payment_method(this)',
        'required': 'false'
    }
    attrs_coin = {
        'placeholder': _('Монета'),
        'class': 'custom-select__select-default',
        'type': 'select',
        'name': 'select',
        'm-balance-change': 'coin',
        'id': 'm-balance-2',
        'onchange': 'set_payment_method(this)',
        'required': 'false'
    }
    place = forms.ChoiceField(widget=forms.Select(attrs=attrs_place), choices=CHOICES_PLACE)
    coin = forms.ChoiceField(widget=forms.Select(attrs=attrs_coin), choices=CHOICES_COIN)

    address = forms.CharField(
        min_length=1,
        max_length=100,
        required=False,
        widget=forms.TextInput(
            attrs={
                'placeholder': _('Tkjw...VWQGF'),
                'class': 'u-input input-el__area',
                'type': 'text',
                'name': "m-balance-3",
                'id': 'm-balance-3',
            }
        )
    )
    total = forms.IntegerField(
        min_value=1,
        widget=forms.TextInput(
            attrs={
                'placeholder': '0',
                'class': 'u-input input-el__area',
                'type': 'text',
                'name': "m-balance-4",
                'id': 'm-balance-4'
            }
        )
    )

    def __init__(self, *args, **kwargs):
        # Принимаем юзера из views
        user = kwargs.pop('ud', None)
        self.user = user
        self.cd = None
        super(Withdrawal, self).__init__(*args, **kwargs)

    def create_transfer(self):
        nt = Transactions()
        nt.from_user = self.user
        nt.total = int(self.cd['total'])
        nt.wallet = self.cd['address']
        nt.type = nt.ORDER_TYPE[1][0]
        nt.type_pay = self.cd['place']
        nt.status = nt.ORDER_STATUS[1][0]
        nt.save()

    def set_status_active(self):
        if self.cd['total'] >= SiteConfiguration.objects.first().entry_fee:
            self.user.verified = True
            self.user.free_sub = True
            self.user.save()

    def clean(self):
        cd = super().clean()
        self.cd = cd
        total = self.user.balance + self.user.bonus_balance
        VE = []
        if not self.user:
            VE.append(ValidationError(_('Нет такого пользователя'), code='not_user'))
        if 'address' not in self.cd or self.cd['address'] == '':
            VE.append(ValidationError(_('Некоректный адрес'), code='not_correct_address'))
        if cd['total'] <= 50:
            VE.append(ValidationError(_('Выводимая сумма меньше 50 USD'), code='total_low50USD'))
        if 0 > int(cd['total']) >= total:
            VE.append(ValidationError(_('Выводимая сумма больше доступой к выводу суммы'), code='not_correct_money'))
        if VE:
            raise ValidationError(VE)
        else:
            self.create_transfer()


class PaymentVerificationAndSendTG(forms.Form):
    payment_verification = forms.CharField()

    def clean(self):
        cleaned_data = super().clean()


class SendMoneyToPool(forms.Form):
    total = forms.CharField(
        max_length=250,
        min_length=8,
        widget=forms.TextInput(
            attrs={
                'class': 'u-input input-el__area',
                'type': "number",
                'placeholder': _('Сумма'),
                'name': 'send-money-to-pool',
                'id': 'ss1',
            }
        )
    )

    def __init__(self, *args, **kwargs):
        # Принимаем юзера из views
        user = kwargs.pop('ud', None)
        pool = kwargs.pop('pool', None)
        if args:
            self.data = args[0]
        self.user = user
        self.pool = pool
        super(SendMoneyToPool, self).__init__(*args, **kwargs)

    def add_pool_money(self):
        self.pool.now_total += float(self.data['total'])
        self.pool.save()
        if self.pool.max_total-self.pool.now_total <= 10:
            self.pool.status = True
            self.pool.data_start = datetime.datetime.now()
            self.pool.save()
        us = PoolUsers.objects.filter(pool=self.pool, user=self.user, take_money=False)
        if not us:
            us = PoolUsers()
            us.pool = self.pool
            us.user = self.user
            us.total = float(self.data['total'])
            us.percent = float(self.data['total'])*100/float(self.pool.max_total)
            us.save()
        else:
            us = us[0]
            us.total += float(self.data['total'])
            us.percent += float(self.data['total']) * 100 / float(self.pool.max_total)
            us.save()
        take_money_from_user(self.user, float(self.data['total']))

    def clean(self):
        cd = super().clean()
        tt = self.user.balance + self.user.bonus_balance
        ost = self.pool.max_total-self.pool.now_total
        if self.pool.status or not self.pool.ended:
            if int(self.data['total']) <= ost:
                if int(self.data['total']) > 0:
                    if int(self.data['total']) <= tt:
                        self.add_pool_money()
                        self._errors = None
                    else:
                        b = round(tt, 2)
                        raise ValidationError(_(f'Сумма для взноса больше вашего балланса {b}'))
                else:
                    raise ValidationError(_('Сумма не должна быть меньше или ровна 0'))
            else:
                raise ValidationError(_(f'Сумма вклада больше свободного места в пуле\nСвободно {ost} USD'))
        else:
            raise ValidationError(_('Данный пул уже в работе'))
