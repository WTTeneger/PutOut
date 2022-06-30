from django.contrib import admin
# Register your models here.
from django.urls import reverse
from django.utils.html import format_html
from solo.admin import SingletonModelAdmin

from .actions import potranslate
from .models import *
from localer import translate_po


class SettingsSite(SingletonModelAdmin):
    fieldsets = (  # Это выводится внутри объекта
        (l_('Personal info'), {'fields': ('site_name', 'total_profit')}),
        (l_('Additionally'), {'fields': ('maintenance_mode', 'entry_fee',)}),
        (l_('Cripto'), {'fields': ('USDT_Address', "USDT_QRCODE")}),
    )

#
# class ProductAdmin(admin.ModelAdmin):
#     list_display = ('title', 'category', 'discount', 'is_active', 'get_link_page', 'count_in_search')  # Что выводится
#     # в главном экране
#     list_display_links = ('title',)
#     search_fields = ('title', 'description')  # поиск ищет по этим полям
#     list_editable = ('category', 'discount', 'is_active', 'count_in_search',)
#     list_filter = ('is_active',)  # Фильтр справа
#     # ordering = ('username',)
#     # filter_horizontal = ('count_in_search',)
#     fieldsets = ( #Это выводится внутри объекта
#         (l_('Personal info'), {'fields': ('name', 'lastname', 'balance')}),
#         (l_('Прочее'), {'fields': ('', 'status', 'data_create')}),


class UserDataAdmin(admin.ModelAdmin):
    def referral_count_friends(self, obj):
        return int(obj.referral.count_friends)

    referral_count_friends.short_description = 'Колличество приглашённых'

    def referral_url(self, obj):
        url = reverse('admin:main_referral_change', args=[obj.referral.id])
        return format_html("<a href='{}'>{}</a>", url, obj.referral.referral_code)

    referral_url.short_description = 'Рефералка'

    list_display = ('mail', 'username', 'account_type', 'verified', 'balance', 'telegram_alert', 'bonus_balance', 'referral_url',
                    'referral_count_friends')  # Что выводится в главном экране
    list_display_links = ('mail', 'username', 'referral_url',)
    search_fields = ('mail', 'account_type')  # поиск ищет по этим полям
    list_editable = ('verified', 'balance', 'bonus_balance', 'telegram_alert',)
    list_filter = ('verified', 'account_type')  # Фильтр справа
    # ordering = ('username',)
    # filter_horizontal = ('count_in_search',)
    # readonly_fields = ('data_reg',)
    fieldsets = (  # Это выводится внутри объекта
        (l_('Персональная информация'), {'fields': ('mail', 'username', 'account_type', 'balance', 'bonus_balance', 'verified', 'telegram_alert', 'free_sub', 'TwoFA')}),
        (l_('Доп инфа'), {'fields': ('api_token', 'from_user', 'courses', 'referral')}),
        (l_('Системные'), {'fields': ('login', 'language')}),
    )


class ProductAdmin(admin.ModelAdmin):
    list_display = ('title', 'price', 'type')  # Что выводится
    # в главном экране
    list_display_links = ('title',)
    search_fields = ('title',)  # поиск ищет по этим полям
    list_editable = ('price',)
    list_filter = ('type',)  # Фильтр справа
    # ordering = ('username',)
    # filter_horizontal = ('count_in_search',)
    readonly_fields = ('data_create',)
    # fieldsets = (  # Это выводится внутри объекта
    #     (l_('Персональная информация'), {'fields': ('title', 'descriptions', 'price')}),
    #     (l_('Доп инфа'), {'fields': ('type', 'platforms', 'orders')}),
    #     (l_('Системные'), {'fields': ('status')}),
    # )


class CourseAdmin(admin.ModelAdmin):
    list_display = ('title', 'price',)  # Что выводится
    # в главном экране
    list_display_links = ('title',)
    search_fields = ('title',)  # поиск ищет по этим полям
    # list_editable = ('title', )
    # list_filter = ('type',)  # Фильтр справа
    # ordering = ('username',)
    # filter_horizontal = ('count_in_search',)
    # readonly_fields = ('data_reg',)
    # fieldsets = (  # Это выводится внутри объекта
    #     (l_('Персональная информация'), {'fields': ('mail', 'account_type', 'balance', 'bonus_balance', 'verified')}),
    #     (l_('Доп инфа'), {'fields': ('api_token', 'from_user', 'courses', 'trader', 'client', 'referral')}),
    #     (l_('Системные'), {'fields': ('login', 'language')}),
    # )


class ReferralAdmin(admin.ModelAdmin):
    list_display = ('referral_code', 'count_friends',)  # Что выводится
    # в главном экране
    list_display_links = ('referral_code',)
    search_fields = ('referral_code',)  # поиск ищет по этим полям
    # list_editable = ('referral_code', )
    # list_filter = ('type',)  # Фильтр справа
    # ordering = ('username',)
    # filter_horizontal = ('count_in_search',)
    # readonly_fields = ('data_reg',)
    # fieldsets = (  # Это выводится внутри объекта
    #     (l_('Персональная информация'), {'fields': ('mail', 'account_type', 'balance', 'bonus_balance', 'verified')}),
    #     (l_('Доп инфа'), {'fields': ('api_token', 'from_user', 'courses', 'trader', 'client', 'referral')}),
    #     (l_('Системные'), {'fields': ('login', 'language')}),
    # )


class SubscriptionsAdmin(admin.ModelAdmin):
    list_display = ('id', 'product', 'client', 'data_start', 'data_end', 'active')  # Что выводится
    # в главном экране
    list_display_links = ('id', 'product', 'client')
    search_fields = ('id', 'product', 'client', 'data_start', 'data_end',)  # поиск ищет по этим полям
    list_editable = ('data_start', 'data_end', 'active')
    list_filter = ('data_start', 'data_end',)  # Фильтр справа
    # ordering = ('username',)
    # filter_horizontal = ('count_in_search',)
    # readonly_fields = ('data_reg',)
    fieldsets = (  # Это выводится внутри объекта
        (l_('Персональная информация'), {'fields': ('client', 'product', 'type', 'active')}),
        (l_('Дата'), {'fields': ('data_start', 'data_end')}),
        # (l_('Системные'), {'fields': ('login', 'language')}),
    )


class ReferralLogsAdmin(admin.ModelAdmin):
    list_display = ('data', 'user', 'partner', 'line', 'result')  # Что выводится
    # в главном экране
    list_display_links = ('data', )
    # search_fields = ()  # поиск ищет по этим полям
    list_editable = ('result',)
    list_filter = ('data', 'line',)  # Фильтр справа
    # ordering = ('username',)
    # filter_horizontal = ('count_in_search',)
    readonly_fields = ('data',)
    # fieldsets = (  # Это выводится внутри объекта
    #     (l_('Персональная информация'), {'fields': ('client', 'product')}),
    #     (l_('Дата'), {'fields': ('data_start', 'data_end')}),
    #     # (l_('Системные'), {'fields': ('login', 'language')}),
    # )


class ProductLogsAdmin(admin.ModelAdmin):
    list_display = ('data', 'product', 'symbol', 'to', 'id_order', 'status')  # Что выводится
    # в главном экране
    list_display_links = ('data',)
    # search_fields = ()  # поиск ищет по этим полям
    # list_editable = ('data_start', 'data_end',)
    list_filter = ('product', 'data', 'status', 'symbol',)  # Фильтр справа
    # ordering = ('username',)
    # filter_horizontal = ('count_in_search',)
    readonly_fields = ('data',)
    # fieldsets = (  # Это выводится внутри объекта
    #     (l_('Персональная информация'), {'fields': ('client', 'product')}),
    #     (l_('Дата'), {'fields': ('data_start', 'data_end')}),
    #     # (l_('Системные'), {'fields': ('login', 'language')}),
    # )


class ProductOrdersAdmin(admin.ModelAdmin):
    list_display = ('data', 'product', 'symbol', 'to', 'PnL', 'ROE', 'status')  # Что выводится
    # в главном экране
    list_display_links = ('data',)
    # search_fields = ()  # поиск ищет по этим полям
    # list_editable = ('data_start', 'data_end',)
    list_filter = ('product', 'data', 'status', 'symbol',)  # Фильтр справа
    # ordering = ('username',)
    # filter_horizontal = ('count_in_search',)
    readonly_fields = ('data',)
    # fieldsets = (  # Это выводится внутри объекта
    #     (l_('Персональная информация'), {'fields': ('client', 'product')}),
    #     (l_('Дата'), {'fields': ('data_start', 'data_end')}),
    #     # (l_('Системные'), {'fields': ('login', 'language')}),
    # )


class VerifyEmailAdmin(admin.ModelAdmin):
    list_display = ('email', 'code', 'date')
    list_filter = ('email', 'code', 'date')


class PoolLogsAdmin(admin.ModelAdmin):
    list_display = ('pool', 'data', 'data_end', 'start_total', 'end_total')
    list_editable = ('data_end', 'start_total', 'end_total',)

class MyAdmin(admin.ModelAdmin):
    actions = [potranslate]


# class TelegramAccountAdmin(admin.ModelAdmin):
#     list_display = ('name', 'tg_id',)
#     list_filter = ('name', 'tg_id',)


admin.site.register(SiteConfiguration, SettingsSite)
admin.site.register(UserData, UserDataAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(APIKeys, )
admin.site.register(TelegramAccount, )
admin.site.register(Transactions, )
admin.site.register(TwoFA, )
# admin.site.register(Client, )
admin.site.register(Course, CourseAdmin)
admin.site.register(Lesson, )
admin.site.register(Logs, )
admin.site.register(Orders, )
admin.site.register(Referral, ReferralAdmin)
admin.site.register(Subscriptions, SubscriptionsAdmin)
admin.site.register(Trader, )
admin.site.register(PoolUsers, )
admin.site.register(Pools, )
admin.site.register(PoolLogs, PoolLogsAdmin)
admin.site.register(ReferralLogs, ReferralLogsAdmin)
admin.site.register(VerifyEmail, VerifyEmailAdmin)
admin.site.register(ProductLogs, ProductLogsAdmin)
admin.site.register(ProductOrders, ProductOrdersAdmin)
