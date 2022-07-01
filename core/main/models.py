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

    maintenance_mode = models.BooleanField(default=False, verbose_name=l_('Режим обслуживания'))

    def __str__(self):
        return "Настройки сайта"


class UserData(models.Model):
    class Meta:
        verbose_name = l_('Данные пользователя')
        verbose_name_plural = l_('Данные пользователей')

    ACCOUNT_TYPE = (
        ('client', 'Клиент'),
    )
    login = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name=l_('Данные авторизации'))
    username = models.CharField(max_length=255, blank=True, null=True, verbose_name=l_('Имя пользователя'))
    mail = models.CharField(null=True, max_length=250, verbose_name='mail')
    verified = models.BooleanField(default=0, verbose_name=l_('Проверка'))
    balance = models.FloatField(default=0, verbose_name=l_('Баланс'), validators=[validate_decimals])
    bonus_balance = models.FloatField(default=0, verbose_name=l_('Бонусный баланс'), validators=[validate_decimals])
    from_user = models.ForeignKey('UserData', null=True, on_delete=models.SET(''), blank=True,
                                  verbose_name=l_('От кого пришёл'))
    inventory = models.ForeignKey('Inventory', null=True, on_delete=models.CASCADE, blank=True,
                                  verbose_name=l_('Инвентарь'))
    stats = models.ForeignKey('Stats', null=True, on_delete=models.CASCADE, blank=True,
                              verbose_name=l_('Статистика'))
    transactions = models.ForeignKey('Transactions', null=True, on_delete=models.CASCADE, blank=True,
                                     verbose_name=l_('Операции'))

    def __str__(self):
        return 'Пользователь №{} {}'.format(self.id, self.mail)


class Inventory(models.Model):
    class Meta:
        verbose_name = l_('Данные пользователя')
        verbose_name_plural = l_('Данные пользователей')

    ACCOUNT_TYPE = (
        ('client', 'Клиент'),
    )
    items = models.ManyToManyField("item", verbose_name=l_('Предметы пользователя'))
    characters = models.ManyToManyField("Character", verbose_name=l_('Персонажи пользователя'))

    def __str__(self):
        return 'инвентарь №{}'.format(self.id)


class Transactions(models.Model):
    class Meta:
        verbose_name = l_('Данные транзации')
        verbose_name_plural = l_('Данные транзаций')

    _TARGET_TRANS = (
        ('purchase', 'purchase'),
        ('replenishment', 'replenishment'),
        ('withdrawal', 'withdrawal'),
    )
    _STATUS_TRANS = (
        ('new', 'Новый'),
        ('inwork', 'В работе'),
        ('end', 'Закончен'),
    )
    uuid = models.UUIDField(default=uuid4(), primary_key=True, auto_created=True, verbose_name=l_('UUID транзации'))
    dateCreate = models.DateTimeField(verbose_name=l_('Дата создания'))
    dateCompiled = models.DateTimeField(verbose_name=l_('Дата окончания'))
    target = models.CharField(max_length=30, choices=_TARGET_TRANS, verbose_name=l_('Цель транзации'))
    status = models.CharField(max_length=30, choices=_STATUS_TRANS, verbose_name=l_('Статус'))
    total = models.FloatField(verbose_name=l_('Сумма'))

    def __str__(self):
        return 'Транзакция №{}'.format(self.id)


class Stats(models.Model):
    class Meta:
        verbose_name = l_('Данные статистики пользователя')
        verbose_name_plural = l_('Данные статистики пользователей')

    ACCOUNT_TYPE = (
        ('client', 'Клиент'),
    )
    # Профиль
    finishedGame = models.IntegerField(default=0, verbose_name=l_('Оконченных игр'))
    takedMoney = models.IntegerField(default=0, verbose_name=l_('Собранно монет'))
    mostTotalCharacters = models.IntegerField(default=0, verbose_name=l_('Самая большая толпа'))
    mostTotalCountMoneyInGame = models.IntegerField(default=0, 
        verbose_name=l_('Самое большое колличество собранных монет за игру'))
    mostTotalCountMoney = models.IntegerField(default=0, verbose_name=l_('Самое большое колличество собранных монет за игру'))
    totalKilometers = models.FloatField(default=0, verbose_name=l_('Пройдено киллометров'))
    pedestriansEaten = models.IntegerField(default=0, verbose_name=l_('Съедено прохожих'))
    timeSpent = models.IntegerField(default=0, verbose_name=l_('Проведено времени'))

    # Смерть 1 персонажа
    byCar = models.IntegerField(default=0, verbose_name=l_('Умер от машин'))
    byHelicopter = models.IntegerField(default=0, verbose_name=l_('Умер от вертолетов'))
    byHole = models.IntegerField(default=0, verbose_name=l_('Умер от ям'))
    byScrolling = models.IntegerField(default=0, verbose_name=l_('Умер от пролистывания'))
    byGroundBomb = models.IntegerField(default=0, verbose_name=l_('Умер от наземных бомб'))
    byAerialBomb = models.IntegerField(default=0, verbose_name=l_('Умер от воздушных бомб'))

    # Игра закончена по причине
    byAerialBomb = models.IntegerField(default=0, verbose_name=l_('Умер от воздушных бомб'))

    # Полученные бонусы
    bonusNinja = models.IntegerField(default=0, verbose_name=l_('Ниндзя'))
    bonusDragon = models.IntegerField(default=0, verbose_name=l_('Ниндзя'))

    def __str__(self):
        return 'Статистика №{}'.format(self.id)


class Item(models.Model):
    class Meta:
        verbose_name = l_('Предмет')
        verbose_name_plural = l_('Предметы')

    _TYPE_ITEM = (
        ('HEAD', 'Голова'),
        ('ARM', 'Руки'),
        ('CHEST', 'Туловище'),
        ('LEGS', 'Ноги'),
        ('WEAPON', 'Оружие'),
        ('SKIN', 'Скин'),
    )
    _RARITY_ITEM = (
        ('UNCOMMON', 'Обычная'),
        ('COMMON', 'Интересная'),
        ('RARE', 'Редкая'),
        ('EPIC', 'Раритетная'),
    )
    type = models.CharField(max_length=200, choices=_TYPE_ITEM, verbose_name=l_('Тип предмета'))
    title = models.CharField(max_length=200, verbose_name=l_('Название предмета'))
    description = models.CharField(max_length=200, verbose_name=l_('Описание'))
    rarity = models.CharField(max_length=200, choices=_RARITY_ITEM, verbose_name=l_('Типы предметов'))
    endurance = models.IntegerField(default=0, verbose_name=l_('Прочность'))
    image = models.CharField(max_length=255, verbose_name=l_('Изображение'))
    owner = models.ForeignKey('UserData', on_delete=models.SET(''), blank=True, null=True, verbose_name=l_('Владелец'))

    def __str__(self):
        return 'Предмет №{}'.format(self.id)


class StoreItem(models.Model):
    class Meta:
        verbose_name = l_('Предмет')
        verbose_name_plural = l_('Предметы')

    _STATUS_STOREITEM = (
        ('new', 'Новый'),
        ('ended', 'Законченный'),
    )
    price = models.FloatField(verbose_name=l_('Цена товара'))
    status = models.CharField(max_length=200, choices=_STATUS_STOREITEM, verbose_name=l_('Типы предметов'))
    owner = models.ForeignKey('UserData', on_delete=models.SET(''), blank=True, null=True, verbose_name=l_('Владелец'))

    def __str__(self):
        return 'Предмет магазина №{}'.format(self.id)


class Character(models.Model):
    class Meta:
        verbose_name = l_('Персонаж')
        verbose_name_plural = l_('Персонажи')

    _TYPE_ITEM = (
        ('HEAD', 'Голова'),
        ('ARM', 'Руки'),
        ('CHEST', 'Туловище'),
        ('LEGS', 'Ноги'),
        ('WEAPON', 'Оружие'),
        ('SKIN', 'Скин'),
    )
    _RARITY_ITEM = (
        ('UNCOMMON', 'Обычная'),
        ('COMMON', 'Интересная'),
        ('RARE', 'Редкая'),
        ('EPIC', 'Раритетная'),
    )
    type = models.CharField(max_length=200, choices=_TYPE_ITEM, verbose_name=l_('Тип предмета'))
    title = models.CharField(max_length=200, verbose_name=l_('Название предмета'))
    level = models.IntegerField(default=0, verbose_name=l_('Описание'))
    skin = models.IntegerField(default=0, verbose_name=l_('Скин'))
    skin = models.IntegerField(default=0, verbose_name=l_('Скин'))
    head = models.OneToOneField('Item', related_name='c_head', on_delete=models.SET(''), null=True, blank=True,
                                verbose_name=l_('Надетый придмет на Голову'))
    arm = models.OneToOneField('Item', related_name='c_arm', on_delete=models.SET(''), null=True, blank=True,
                               verbose_name=l_('Надетый придмет на Руки'))
    chest = models.OneToOneField('Item', related_name='c_chest', on_delete=models.SET(''), null=True, blank=True,
                                 verbose_name=l_('Надетый придмет на Грудь'))
    legs = models.OneToOneField('Item', related_name='c_legs', on_delete=models.SET(''), null=True, blank=True,
                                verbose_name=l_('Надетый придмет на Ноги'))
    weapon = models.OneToOneField('Item', related_name='c_weapon', on_delete=models.SET(''), null=True, blank=True, verbose_name=l_('Оружие'))

    def __str__(self):
        return 'Персонаж №{}'.format(self.id)
