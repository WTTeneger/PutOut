from tg_bot import *
from ..main.models import SiteConfiguration, ReferralLogs, TelegramAccount
from ..main.text_to_tg import *
from django.utils.translation import gettext_lazy as l_


def recording_logs(partner, descriptions='', total=0):
    """
    Функция записи логов для польозателя

    partner: Основное лицо записи
    description: Описание (При регистрации registration)
    total: Общая сумма действия(При рег 150, при пополнение сумма его)
    """

    def create_ReferralLogs(partner_, referral_, line_, descriptions_, result_):
        RL = ReferralLogs()
        RL.user = referral_
        RL.partner = partner_
        RL.line = str(line_)
        RL.descriptions = descriptions_
        RL.result = result_
        RL.save()

    referral = partner
    sl_ = {
        1: float(total) / 100 * 15,
        2: float(total) / 100 * 10,
        3: float(total) / 100 * 5,
    }
    for el in range(1, 4):
        referral = referral.from_user
        if referral:
            result = '{}'.format(sl_[el])
            create_ReferralLogs(partner, referral, el, descriptions, result)
        else:
            break


def distribution_of_money(user, money):
    """
    :param user: Кто оплатит
    :param money: Сколько оплатил
    :return: распределит деньги
    """

    def add_money(bonus_user, bonus_money):
        """
        :param bonus_user: Кому зачислить
        :param bonus_money: сколько зачислить
        :return: Зачислит пользователю
        """
        bonus_user.bonus_balance = float(bonus_user.bonus_balance) + float(bonus_money)

        bonus_user.save()

    percent = money / 100
    company_percent = 40 * percent
    # TODO: Понять что за 30 процентов user
    user_percent = 30 * percent
    referral_dict = {
        # линия: бонус
        1: 15 * percent,
        2: 10 * percent,
        3: 5 * percent
    }
    add_money(user, money)
    no_active_money = 0
    for el in range(1, 4):
        if user.from_user:
            user = user.from_user
            add_money(user, referral_dict[el])
            for token in TelegramAccount.objects.filter(owner=user):
                send_message([token.tg_token], (l_(referral_link_pay).format(el, referral_dict[el])))

        else:
            no_active_money += referral_dict[el]
    SC = SiteConfiguration.objects.get()
    SC.total_profit = SC.total_profit + (no_active_money + company_percent + user_percent)
    SC.save()


def take_money_from_user(us, p_price):
    totals_money = us.bonus_balance + us.balance
    if totals_money >= p_price:

        if us.bonus_balance > 0:
            if us.bonus_balance >= p_price:
                us.bonus_balance -= p_price
                p_price = 0
                us.save()
            else:
                p_price -= us.bonus_balance
                us.bonus_balance = 0
                us.save()
        if p_price > 0:
            us.balance -= p_price
            p_price = 0
        us.save()
        return True
    else:
        return False
