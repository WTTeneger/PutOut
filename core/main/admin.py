from django.contrib import admin
# Register your models here.
from django.urls import reverse
from django.utils.html import format_html
from solo.admin import SingletonModelAdmin

from .models import *


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
# admin.site.register(ProductOrders, )
