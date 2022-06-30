import datetime
import time
from uuid import uuid4

from django.conf import settings
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import Avg, Count, Sum, Q
from django.db.models.functions import ExtractDay
from django.utils.timezone import now
from django.utils.translation import gettext_lazy as l_
from solo.models import SingletonModel


def validate_decimals(value):
    try:
        return round(float(value), 2)
    except:
        raise ValidationError(
            l_('%(value)s is not an integer or a float  number'),
            params={'value': value},
        )


class IntegerRangeField(models.IntegerField):
    def __init__(self, verbose_name=None, name=None, min_value=None, max_value=None, **kwargs):
        self.min_value, self.max_value = min_value, max_value
        models.IntegerField.__init__(self, verbose_name, name, **kwargs)

    def formfield(self, **kwargs):
        defaults = {'min_value': self.min_value, 'max_value': self.max_value}
        defaults.update(kwargs)
        return super(IntegerRangeField, self).formfield(**defaults)


class SiteConfiguration(SingletonModel):
    class Meta:
        verbose_name = l_("Настройки сайта")

    entry_fee = models.PositiveIntegerField(default=150, verbose_name=l_('Стартовый взнос'))
    site_name = models.CharField(max_length=255, default=l_('Название сайта'))
    USDT_Address = models.CharField(max_length=255, blank=True, verbose_name=l_('Адрес кошелька для оплаты'))
    USDT_QRCODE = models.ImageField(max_length=255, blank=True, verbose_name=l_('QR Code'))
    maintenance_mode = models.BooleanField(default=False, verbose_name=l_('Режим обслуживания'))
    total_profit = models.FloatField(default=0, verbose_name=l_('Прибыль'),
                                     validators=[validate_decimals])

    def __str__(self):
        return "Настройки сайта"


class UserData(models.Model):
    class Meta:
        verbose_name = l_('Данные пользователя')
        verbose_name_plural = l_('Данные пользователей')

    ACCOUNT_TYPE = (
        ('trader', 'Трейдер'),
        ('client', 'Клиент'),
    )
    login = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name=l_('Данные авторизации'))

    username = models.CharField(max_length=255, blank=True, null=True, verbose_name=l_('Имя пользователя'))
    mail = models.CharField(null=True, max_length=250, verbose_name='mail')
    verified = models.BooleanField(default=0, verbose_name=l_('Проверка'))
    free_sub = models.BooleanField(default=0, verbose_name=l_('Бесплатная подписка'))
    balance = models.FloatField(default=0, verbose_name=l_('Баланс'), validators=[validate_decimals])
    bonus_balance = models.FloatField(default=0, verbose_name=l_('Бонусный баланс'), validators=[validate_decimals])
    api_token = models.ManyToManyField('APIKeys', blank=True, verbose_name=l_('Токены бирж'))
    from_user = models.ForeignKey('UserData', null=True, on_delete=models.SET(''), blank=True,
                                  verbose_name=l_('От кого пришёл'))
    courses = models.ManyToManyField('Course', blank=True, verbose_name=l_('Доступные курсы'))
    account_type = models.CharField(default='client', max_length=250, choices=ACCOUNT_TYPE,
                                    verbose_name=l_('Тип аккаунта'))
    products = models.ManyToManyField('Product', verbose_name=l_('Продукты'))
    referral = models.ForeignKey('Referral', null=True, on_delete=models.CASCADE, blank=True,
                                 verbose_name=l_('Рефералка'))
    language = models.CharField(max_length=10,
                                choices=settings.LANGUAGES,
                                default=settings.LANGUAGE_CODE)
    TwoFA = models.ForeignKey("TwoFA", null=True, on_delete=models.SET(''), blank=True, verbose_name=l_('2 FA'))

    telegram_alert = models.BooleanField(default=True, verbose_name=l_('Уведомление в тг'))

    def __str__(self):
        return 'Пользователь №{} {}'.format(self.id, self.mail)


class TwoFA(models.Model):
    class Meta:
        verbose_name = l_('Данные 2FA')

    code = models.CharField(max_length=30, verbose_name=l_('Код генерации'))
    qr_url = models.ImageField(verbose_name=l_('QRCODE'), upload_to='qrcode')
    verificated = models.BooleanField(default=False)

    def __str__(self):
        return 'Данные 2FA №{}'.format(self.id)


class APIKeys(models.Model):
    class Meta:
        verbose_name = l_('API ключ')
        verbose_name_plural = l_('API ключи')

    PLACE_TYPE = (
        ('Binance', 'Binance'),
        ('ByByt', 'ByBit'),
    )

    owner = models.ForeignKey("UserData", null=True, blank=True, on_delete=models.CASCADE, verbose_name=l_('Владелец'))
    data_create = models.DateTimeField(auto_now_add=True, verbose_name=l_('Дата создания'))
    place = models.CharField(choices=PLACE_TYPE, max_length=250, verbose_name=l_('Площадка'))
    title = models.CharField(default='', max_length=250, verbose_name=l_('Название'))
    key_public = models.CharField(max_length=250, verbose_name=l_('Публичный ключ'))
    key_private = models.CharField(max_length=250, verbose_name=l_('Приватный ключ'))
    status = models.BooleanField(default=True, verbose_name=l_('Активен ли'))

    def __str__(self):
        return 'Ключи от платформы {} №{}'.format(self.place, self.id)


class Referral(models.Model):
    class Meta:
        verbose_name = l_('Рефералка')
        verbose_name_plural = l_('Рефералки')

    referral_code = models.CharField(max_length=250, verbose_name=l_('Код приглашения'))
    count_friends = models.IntegerField(verbose_name=l_('Колличество приглашений'))
    line_1 = models.ManyToManyField("UserData", related_name='line_1', verbose_name=l_('Линия 1'))
    line_2 = models.ManyToManyField("UserData", related_name='line_2', verbose_name=l_('Линия 2'))
    line_3 = models.ManyToManyField("UserData", related_name='line_3', verbose_name=l_('Линия 3'))

    def __str__(self):
        return 'Реферальная система кода {}'.format(self.referral_code)


class Course(models.Model):
    class Meta:
        verbose_name = l_('Курс')
        verbose_name_plural = l_('Курсы')

    title = models.CharField(max_length=250, verbose_name=l_('Название'))
    price = models.IntegerField(default=0, verbose_name=l_('Цена'))
    lessons = models.ManyToManyField('Lesson', verbose_name=l_('Уроки'))

    def __str__(self):
        return 'Курс {}'.format(self.title)


class Lesson(models.Model):
    class Meta:
        verbose_name = l_('Урок из курса')
        verbose_name_plural = l_('Уроки из курсов')

    html = models.TextField(verbose_name=l_('HTML'))

    def __str__(self):
        return 'Урок №{}'.format(self.id)


class Product(models.Model):
    class Meta:
        verbose_name = l_('Продукт')
        verbose_name_plural = l_('Продукты')

    PRODUCT_TYPE = (
        ('futures', 'Фьючерсы'),
        ('spot', 'Спот'),
    )
    data_create = models.DateTimeField(auto_now_add=True, verbose_name=l_('Дата создания'))
    title = models.CharField(max_length=250, verbose_name=l_('Название'))
    price = IntegerRangeField(default=0, min_value=50, max_value=500, verbose_name=l_('Цена'))
    descriptions = models.CharField(blank=True, max_length=1000, verbose_name=l_('Описание'))
    type = models.CharField(blank=True, max_length=250, choices=PRODUCT_TYPE, verbose_name=l_('Тип'))
    orders = models.ManyToManyField('Orders', blank=True, verbose_name=l_('Ордера'))
    platforms = models.ForeignKey('APIKeys', blank=True, null=True, on_delete=models.SET(None),
                                  verbose_name=l_('Токеты платформы'))
    status = models.BooleanField(default=True, verbose_name=l_('Статусы'))

    def all_stats(self):
        def mdy_to_ymd(d):
            # return "{}-{}-{}".format(d.year, d.month, d.day)
            unixtime = int(time.mktime(d.timetuple()))*1000
            return unixtime
        stats = {}
        orders = ProductOrders.objects.filter(product=self).order_by('-data_end')
        current_datetime = now()
        nd = current_datetime - datetime.timedelta(days=31)
        qs = orders.filter(
            data__gt=nd,
        )
        stats['orders'] = qs
        sub = Subscriptions.objects.filter(product=self, type='tg')
        stats['sub'] = sub
        stats['followers'] = Subscriptions.objects.filter(product=self, type='copy')
        orders_ud = orders.filter(Q(status='END') | Q(status='CANCELED'))
        ROE = []
        for el in orders_ud:
            el.start_price = el.start_price if el.start_price != None else 0
            el.ROE = float(round(el.ROE, 2)) if el.ROE else 0
            ROE.append(el.ROE)
        stats['all_orders'] = orders_ud
        stats['avg_ROE'] = float(round(qs.aggregate(Avg('ROE'))['ROE__avg'], 3)) if \
            qs.aggregate(Avg('ROE'))[
            'ROE__avg'] else 0
        # stats['sum_ROE'] = float(round(orders.aggregate(Avg('ROE'))['ROE__avg'], 3))
        stats['month_ROE'] = float(round(qs.aggregate(total=Sum('ROE'))['total'], 2)) if \
            qs.aggregate(total=Sum('ROE'))[
                'total'] else 0
        stats['avg_PnL'] = float(round(qs.aggregate(Avg('PnL'))['PnL__avg'], 3)) if \
            qs.aggregate(Avg('PnL'))[
                'PnL__avg'] else 0
        stats['avg_leverage'] = float(round(qs.aggregate(Avg('leverage'))['leverage__avg'], 3)) if \
            qs.aggregate(Avg('leverage'))['leverage__avg'] else 0
        stats['main_symbol'] = qs.annotate(Count('symbol'))[0].symbol if \
            qs.annotate(Count('symbol')) else l_('Ещё нет')
        stats['month_count'] = len(qs.annotate(day=ExtractDay("data")).values("day"))
        stats['total_count'] = len(orders)
        dt = [el.ROE if el.ROE is not None else 0 for el in qs]
        dts = [[mdy_to_ymd(el.data), str(el.ROE).replace(',', '.')] for el in orders if el.ROE]
        stats['all_ROE'] = dt if len(dt) > 0 else [0, 0]
        stats['all_ROE_DATA'] = dts if dts else [[int(time.time()), 0]]
        stats['count_true_ROE'] = len([el for el in stats['all_ROE'] if el > 0])
        stats['count_false_ROE'] = len(stats['all_ROE']) - stats['count_true_ROE']
        d_today = datetime.datetime.today().replace(tzinfo=None)
        d_create = self.data_create.replace(tzinfo=None)
        d_calc = d_today - d_create
        count_day = d_calc.days + 1
        stats['day_in_market'] = count_day
        if stats['count_true_ROE'] != 0:
            if stats['count_false_ROE'] != 0:
                stats['risk'] = stats['count_true_ROE'] / stats['count_false_ROE'] * 100 if len(stats['all_ROE']) > 0 else \
                    l_('Ещё нет')
            else:
                stats['risk'] = 0
        else:
            stats['risk'] = l_('Ещё нет')


        stats['count_in_day'] = round(len(orders) / count_day, 1)
        return stats

    def __str__(self):
        return 'Продукт {}'.format(self.title)


class Trader(models.Model):
    class Meta:
        verbose_name = l_('Трейдер')
        verbose_name_plural = l_('Трейдеры')

    products = models.ManyToManyField('Product', verbose_name=l_('Продукты'))

    def __str__(self):
        return 'Трейдер №{}'.format(self.id)


class Orders(models.Model):
    class Meta:
        verbose_name = l_('Сделка')
        verbose_name_plural = l_('Сделки')

    ORDER_FROM = (
        ('user', 'Пользователь'),
        ('product', 'Продукт'),
    )

    date = models.DateTimeField(blank=True, default=None, null=True, verbose_name=l_('Дата'))
    coin = models.CharField(max_length=20, verbose_name=l_('Монета'))
    direction = models.CharField(max_length=20, default='BUY', verbose_name=l_('Направление'))
    start_price = models.FloatField(verbose_name=l_('Цена на входе'))
    end_price = models.FloatField(null=True, blank=True, verbose_name=l_('Цена на выходе'))

    percent = models.FloatField(null=True, blank=True, verbose_name=l_('PNL'))

    order_from = models.CharField(max_length=30, default=None, blank=True, choices=ORDER_FROM,
                                  verbose_name=l_('От кого ордер'))

    def __str__(self):
        return 'Трейдер №{}'.format(self.id)


class Subscriptions(models.Model):
    class Meta:
        verbose_name = l_('Подписка')
        verbose_name_plural = l_('Подписки')

    TYPE_FOLLOWER = (
        ('copy', l_('Копитрейдинг')),
        ('tg', l_('Телеграм')),
    )

    data_start = models.DateField(blank=True, null=True, verbose_name=l_('Дата подписки'))
    data_end = models.DateField(blank=True, null=True, verbose_name=l_('Дата окончания'))
    type = models.CharField(max_length=100, blank=True, default='copy', verbose_name=l_('Тип подписки'))
    product = models.ForeignKey("Product", null=True, blank=True, on_delete=models.SET(''), verbose_name=l_('Продукт'))
    client = models.ForeignKey("UserData", blank=True, null=True, related_name='client_sub', on_delete=models.SET(''),
                               verbose_name=l_('Клиент'))
    percent = IntegerRangeField(default=100, min_value=10, max_value=500, verbose_name=l_('Процент работы'))
    active = models.BooleanField(default=True, verbose_name=l_('Активная'))

    def __str__(self):
        return 'Подписка на {} пользователем {}'.format(self.product.title, self.client)


class ReferralLogs(models.Model):
    class Meta:
        verbose_name = l_('Реферальные логи')
        verbose_name_plural = l_('Реферальные логи')

    LINE_TYPE = (
        ('1', '1'),
        ('2', '2'),
        ('3', '3'),
    )
    data = models.DateTimeField(auto_now_add=True, verbose_name=l_('Дата создания'))
    user = models.ForeignKey('UserData', related_name='user', on_delete=models.CASCADE,
                             verbose_name=l_('Владелец лога'))
    partner = models.ForeignKey('UserData', related_name='partner', on_delete=models.SET(''),
                                verbose_name=l_('Партнёр'))
    line = models.CharField(max_length=50, choices=LINE_TYPE, verbose_name=l_('Линия'))
    descriptions = models.CharField(max_length=50, default='', verbose_name=l_('Описание'))
    result = models.CharField(max_length=250, verbose_name=l_('Результат'))

    def __str__(self):
        return 'ReferralLogs {}'.format(self.user)


class Logs(models.Model):
    class Meta:
        verbose_name = l_('Логи')
        verbose_name_plural = l_('Логи')

    data = models.DateTimeField(verbose_name=l_('Дата создания'))
    user = models.ForeignKey('UserData', on_delete=models.SET(''), verbose_name=l_('Пользователи'))

    def __str__(self):
        return 'Logs №{}'.format(self.id)


class VerifyEmail(models.Model):
    class Meta:
        verbose_name = l_('Верификация Email')
        verbose_name_plural = l_('Верификация Email')

    email = models.CharField(max_length=250, verbose_name='Email пользователя')
    code = models.CharField(max_length=6, verbose_name='Код для подтверждения')
    date = models.DateTimeField(auto_now=True, verbose_name='Дата создание кода')

    def __str__(self):
        return '{}-{}'.format(self.email, self.code)


class ProductLogs(models.Model):
    class Meta:
        verbose_name = l_('Логи продукта')
        verbose_name_plural = l_('Логи продуктов')

    data = models.DateTimeField(auto_now_add=True, verbose_name=l_('Дата создания'))
    product = models.ForeignKey("Product", null=True, on_delete=models.CASCADE, verbose_name=l_('Продукт'))
    symbol = models.CharField(max_length=15, verbose_name=l_('Пара'))
    to = models.CharField(max_length=15, default='', verbose_name=l_('Направление'))
    id_order = models.CharField(max_length=15, verbose_name=l_('id'))
    status = models.CharField(max_length=20, verbose_name=l_('Статус'))

    def __str__(self):
        return 'ProductLogs №{}'.format(self.product.title)


class ProductOrders(models.Model):
    class Meta:
        verbose_name = l_('Ордер продукта')
        verbose_name_plural = l_('Ордера продуктов')

    data = models.DateTimeField(auto_now_add=True, verbose_name=l_('Дата создания'))
    data_end = models.DateTimeField(default=datetime.datetime.today(), verbose_name=l_('Дата завершения'))
    product = models.ForeignKey("Product", null=True, on_delete=models.CASCADE, verbose_name=l_('Продукт'))
    symbol = models.CharField(max_length=15, verbose_name=l_('Пара'))
    to = models.CharField(max_length=15, default='', verbose_name=l_('Направление'))
    id_order = models.IntegerField(verbose_name=l_('id'))
    start_price = models.FloatField(null=True, blank=True, verbose_name=l_('Цена входа'))
    end_price = models.FloatField(null=True, blank=True, verbose_name=l_('Цена выхода'))
    leverage = models.IntegerField(null=True, blank=True, verbose_name=l_('Плечо'))
    size = models.FloatField(default=0, verbose_name=l_('Размер'))
    PnL = models.FloatField(null=True, blank=True, verbose_name=l_('Нереализованная прибыль или убыток'))
    ROE = models.FloatField(null=True, blank=True, verbose_name=l_('Процент прибыли или убытков'))
    status = models.CharField(max_length=20, verbose_name=l_('Статус'))

    def __str__(self):
        return 'ProductOrders №{}'.format(self.id)


class Transactions(models.Model):
    class Meta:
        verbose_name = l_('История транзакции')
        verbose_name_plural = l_('История транзакций')

    ORDER_TYPE = (
        ('1', l_('Пополнение')),
        ('2', l_('Вывод')),
        ('3', l_('Покупка')),

    )
    ORDER_TYPE_PAY = (
        ('Crypto', l_('Криптой')),
        ('Card', l_('Картой')),
        ('Balance', l_('Балансом')),
    )

    ORDER_STATUS = (
        ('1', l_('В ожидании')),
        ('2', l_('Ожидает проверки')),
        ('3', l_('Отменён')),
        ('4', l_('Завершён')),
        ('5', l_('Готово')),
    )
    uuid = models.UUIDField(primary_key=True, default=uuid4, editable=False, unique=True, verbose_name=l_('id ордера'))
    data = models.DateTimeField(auto_now_add=True, verbose_name=l_('Дата создания'))
    data_end = models.DateTimeField(blank=True, null=True, verbose_name=l_('Дата окончания'))
    descriptions = models.CharField(max_length=35, default='', verbose_name=l_('Описание'))
    from_user = models.ForeignKey('UserData', default=None, null=True, blank=True, on_delete=models.CASCADE, verbose_name=l_('Пользователь'))
    total = models.IntegerField(null=True, blank=True, verbose_name=l_('Сумма'))
    wallet = models.CharField(null=True, blank=True, max_length=100, verbose_name=l_('Коешлёк'))
    type = models.CharField(max_length=25, choices=ORDER_TYPE, verbose_name=l_('Тип'))
    payment_url = models.CharField(max_length=500, default='', null=True, blank=True, verbose_name=l_('Сылка оплаты'))
    type_pay = models.CharField(max_length=25, null=True, blank=True, choices=ORDER_TYPE_PAY, verbose_name=l_('Способ'))
    status = models.CharField(max_length=25, choices=ORDER_STATUS, verbose_name=l_('Статус'))
    def __str__(self):
        return 'Transactions №{}'.format(self.uuid)


class TelegramAccount(models.Model):
    class Meta:
        verbose_name = l_('Телеграм токен')
        verbose_name_plural = l_('Телеграм токены')

    data = models.DateTimeField(auto_now_add=True, verbose_name=l_('Дата создания'))
    title = models.CharField(max_length=25, verbose_name=l_('Название'))
    owner = models.ForeignKey('UserData', null=True, blank=True, on_delete=models.CASCADE, verbose_name=l_('Владелец'))
    tg_token = models.CharField(max_length=25, default='', verbose_name=l_('TG token'))

    def __str__(self):
        return 'TelegramAccount №{} - {}'.format(self.id, self.title)


class Pools(models.Model):
    class Meta:
        verbose_name = l_('Пул')
        verbose_name_plural = l_('Пулы')

    data = models.DateTimeField(auto_now_add=True, verbose_name=l_('Дата начала'))
    data_end = models.DateTimeField(auto_now_add=True, verbose_name=l_('Дата окончания'))
    title = models.CharField(max_length=25, verbose_name=l_('Название'))
    now_total = models.FloatField(default=0, verbose_name=l_('сумма сейчас'))
    data_start = models.DateField(null=True, blank=True, verbose_name=l_('Дата старта'))
    max_total = models.FloatField(default=0, verbose_name=l_('Цель'))
    total_day = models.PositiveIntegerField(default=0, verbose_name=l_('Сумма в днях'))
    users = models.ManyToManyField(to='PoolUsers', blank=True, verbose_name=l_('Участники'))
    rating = models.FloatField(default=10, verbose_name=l_('Рейтинг'))
    status = models.BooleanField(default=False, verbose_name=l_('В работе'))
    ended = models.BooleanField(default=False, verbose_name=l_('Зверешен'))

    def __str__(self):
        return 'Пул №{} - {}'.format(self.id, self.title)


class PoolLogs(models.Model):
    class Meta:
        verbose_name = l_('Логи пул')
        verbose_name_plural = l_('Логи пула')

    pool = models.ForeignKey('Pools', on_delete=models.CASCADE, verbose_name=l_('Пулл'))
    data = models.DateTimeField(auto_now_add=True, verbose_name=l_('Дата начала'))
    data_end = models.DateTimeField(verbose_name=l_('Дата окончания'))
    start_total = models.CharField(max_length=25, verbose_name=l_('Сумма на старте'))
    end_total = models.FloatField(default=0, verbose_name=l_('Сумма в конце'))

    def __str__(self):
        return 'Логи пула №{}'.format(self.pool.id)


class PoolUsers(models.Model):
    class Meta:
        verbose_name = l_('Участник пула')
        verbose_name_plural = l_('Участники пула')

    pool = models.ForeignKey('Pools', on_delete=models.CASCADE, verbose_name=l_('Пулл'))
    user = models.ForeignKey('UserData', on_delete=models.CASCADE, verbose_name=l_('Участник'))
    total = models.FloatField(default=0, verbose_name=l_('Сумма вклада'))
    percent = models.FloatField(default=0, verbose_name=l_('Процент вклада'))
    take_money = models.BooleanField(default=0, verbose_name=l_('Получил ли деньги'))

    def __str__(self):
        return 'Участник пулла №{} - {}'.format(self.pool.id, self.user.username)
