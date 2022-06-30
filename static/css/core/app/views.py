import datetime as dt
from copy import deepcopy
import json
from urllib.request import urlopen, urlretrieve

from dateutil.relativedelta import relativedelta
from django.contrib.auth import logout
from django.core.files import File
from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect, render
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view

from core.app.thirdparty_functions import *
from core.main.models import *
from services.twofactorauth import TwoFactorAuth
from tg_bot import send_message, send_admin_message
from .forms import (APIKeysForm, NewTransfer, PasswordChange, TGKeysForm,
                    UserNameChange, TwoFactorAuthForm, Withdrawal, SendMoneyToPool)
from ..main.templatetags.tag_library import get_item
from ..utils.utils import __check_auth, __check_registers, __apikeys


# from unittest import removeResult


# def appDashboard(request):
#     return HttpResponse("return this string")

def getResponceApi(request, data: dict):
    return_data = {'text': '',
                   'reload': False}
    return_data = {**return_data}
    return {**return_data, **data}

@__check_auth
def getUserData(request, data: dict):
    """Объединяем данные пользователя с нашими данными"""
    return_data = {}
    _user = UserData.objects.filter(login=request.user)
    if _user:
        user = _user.values()[0]
        user['api_token'] = True if _user[0].api_token.filter(status=True) else False
        if TwoFA.objects.filter(id=user['TwoFA_id']):
            user['TwoFA'] = TwoFA.objects.filter(id=user['TwoFA_id'])[0]
        return_data = {**return_data, **user}
    return {**return_data, **data}


@api_view(['GET'])
@__check_auth  # Декоратор проверки авторизации
@__check_registers  # Декоратор проверки оплаты входа
def appDashboard(request):
    apikeys = APIKeys.objects.filter(owner__login=request.user).exists()
    return render(request,
                  context=getUserData(request,
                                      {'app': 'appDashboard', 'apikeys': apikeys}),
                  template_name='app/dashboard.html')


# # @api_view(['GET'])
# @__check_auth  # Декоратор проверки авторизации
# # @__check_registers  # Декоратор проверки оплаты входа
# def appStrategy(request):
#     strategyes = Product.objects.filter(status=True)

#     for el in strategyes:
#         el.stats = el.all_stats()
#     dta = {'app': 'appStrategy',
#            'strategyes': strategyes[3:],
#            'topstrategyes': strategyes[:3]}
#     return render(request,
#                   context=getUserData(request, dta),
#                   template_name='app/account_v22.html')

# @api_view(['GET'])
@__check_auth  # Декоратор проверки авторизации
@__check_registers  # Декоратор проверки оплаты входа
def appStrategy(request):
    strategyes = Product.objects.filter(status=True)
    for el in strategyes:
        el.stats = el.all_stats()
    dta = {'app': 'appStrategy',
           'strategyes': strategyes[3:],
           'topstrategyes': strategyes[:3]}
    return render(request,
                  context=getUserData(request, dta),
                  template_name='app/account_v22.html')


@__check_auth  # Декоратор проверки авторизации
# @__check_registers  # Декоратор проверки оплаты входа
@__apikeys
def appStrategyId(request, strategy_id=None):
    """Стр стратегии"""
    if not strategy_id:
        next = request.META.get('HTTP_REFERER')
        return redirect(next)
    strategyes = Product.objects.filter(id=strategy_id)
    # Проверка существования стратегии
    if strategyes.exists():
        for el in strategyes:
            el.stats = el.all_stats()
        strategyes = strategyes[0]
        dta = {'app': 'appStrategy',
               's': strategyes}
        return render(request,
                      context=getUserData(request, dta),
                      template_name='app/trader.html')
    return redirect('appDashboard')


@csrf_exempt
@api_view(['POST'])
@__check_auth  # Декоратор проверки авторизации
# @__check_registers  # Декоратор проверки оплаты входа
def appStrategySwitchStatus(request, strategy_id=None):
    """Включить выключить копирование стратегии"""
    s = Subscriptions.objects.filter(client__login=request.user, id=strategy_id)
    if s:
        s[0].active = not s[0].active
        s[0].save()
        return JsonResponse(getResponceApi(request, {'text': l_('Change Status'), 'switch': True}),
                            content_type="application/json", status=200)
    return JsonResponse(getResponceApi(request, {'text': l_('Not founds subs')}),
                        content_type="application/json", status=404)


@csrf_exempt
@api_view(['POST'])
@__check_auth  # Декоратор проверки авторизации
# @__check_registers  # Декоратор проверки оплаты входа
def appTelegramAlertSwitch(request):
    """Включить выключить копирование стратегии"""
    s = UserData.objects.filter(login=request.user)
    if s:
        s = s[0]
        s.telegram_alert = not s.telegram_alert
        s.save()
        return JsonResponse(getResponceApi(request, {'text': l_('Change Status'), 'switch': True}),
                            content_type="application/json", status=200)
    return JsonResponse(getResponceApi(request, {'text': l_('Not founds subs')}),
                        content_type="application/json", status=404)


@__check_auth  # Декоратор проверки авторизации
@__check_registers  # Декоратор проверки оплаты входа
@__apikeys
def appStrategyFollowId(request, typer='copy', strategy_id=None):
    global T
    us = UserData.objects.filter(login=request.user)
    st = Product.objects.filter(id=strategy_id)
    next = request.META.get('HTTP_REFERER')
    sft = True
    desc = ''
    if us and st:
        us = us[0]
        st = st[0]

        if typer == 'copy':
            desc = l_('Подписался на автокорипрование сделок продукта {}').format(st.title)
            totals_money = us.bonus_balance + us.balance
            p_price = st.price
            T = False
            if totals_money >= p_price or us.free_sub:
                if us.free_sub:
                    us.free_sub = False
                    T = True
                else:
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

                NS = Subscriptions.objects.filter(product=st)
                if NS:
                    NS = NS[0]
                    NS.data_end = NS.data_end + relativedelta(months=1)
                else:
                    NS = Subscriptions()
                    NS.client = us
                    NS.product = st
                    NS.data_end = dt.datetime.now() + dt.timedelta(days=30)
                NS.save()
                us.save()
                st.save()

        else:
            NS = Subscriptions.objects.filter(product=st, type='tg')
            if NS:
                NS = NS[0]
                NS.delete()
                sft = False
            else:
                NS = Subscriptions()
                desc = l_('Подписался на сигналы от продукта {}').format(st.title)
                NS.client = us.client
                NS.product = st
                NS.type = 'tg'
                NS.save()
        if sft:
            new_TR = Transactions()
            new_TR.data_end = dt.datetime.now()
            new_TR.from_user = UserData.objects.filter(login=request.user)[0]
            if T:
                tot = 0
            else:
                tot = -st.price if typer == 'copy' else 0
            new_TR.total = tot
            new_TR.type = Transactions.ORDER_TYPE[0][0]
            new_TR.descriptions = desc
            new_TR.type = Transactions.ORDER_TYPE[2][0]
            new_TR.type_pay = Transactions.ORDER_TYPE_PAY[2][0]
            new_TR.status = Transactions.ORDER_STATUS[4][0]
            new_TR.save()
    return redirect(next)


@api_view(['GET', 'POST'])
@__check_auth  # Декоратор проверки авторизации
@__check_registers  # Декоратор проверки оплаты входа
def appSettings(request):
    tg = TelegramAccount.objects.filter(owner=UserData.objects.filter(login=request.user).first())
    subscriptions = Subscriptions.objects.filter(client=UserData.objects.filter(login=request.user).first())
    data = getUserData(request, {'app': 'appSettings', 'tg': tg, 'languages': settings.LANGUAGES})
    if 'password-change' in request.POST:
        # Форма смены пароля
        PC_form = PasswordChange(request.POST, user_id=request.user)
        if PC_form.is_valid():
            user = User.objects.get(username=request.user)
            user.set_password(PC_form.cleaned_data['new_password'])
            user.save()
            logout(request)
            return redirect('sign-in')
    else:
        PC_form = PasswordChange()

    if 'change-username' in request.POST:
        # Форма смены username
        UNC_form = UserNameChange(request.POST)
        if UNC_form.is_valid():
            user = UserData.objects.get(mail=request.user)
            user.username = UNC_form.cleaned_data['login']
            user.save()
            return redirect('appSettings')
    else:
        UNC_form = UserNameChange()

    data['PC_form'] = PC_form
    data['UNC_form'] = UNC_form
    data['subscriptions'] = subscriptions
    return render(request, 'app/settings.html', data)


@csrf_exempt
# @api_view(['POST'])
@__check_auth  # Декоратор проверки авторизации
def appSetPercent(request, id_sub=None):
    if request.method == 'GET':
        return redirect('appDashboard')
    print(id_sub)
    print(request.POST['value'])
    print(request.POST['value'].isnumeric())

    sub = Subscriptions.objects.filter(id=int(id_sub))
    # print(request.)

    if id_sub and sub and 'value' in request.POST:
        try:
            int(request.POST['value'])
        except:
            return JsonResponse(getResponceApi(request, {'text': l_('Not founds subs')}),
                                content_type="application/json", status=404)
        sub = sub[0]
        if int(request.POST['value']) <= 10:
            v = 10
        elif int(request.POST['value']) >= 500:
            v = 500
        else:
            v = int(request.POST['value'])
        sub.percent = v
        sub.save()
        return JsonResponse(getResponceApi(request, {'text': l_('Change Percent'), 'switch': True}),
                            content_type="application/json", status=200)
    else:
        return JsonResponse(getResponceApi(request, {'text': l_('Not founds subs')}),
                            content_type="application/json", status=404)


@api_view(['GET', 'POST'])
@__check_auth  # Декоратор проверки авторизации
@__check_registers  # Декоратор проверки оплаты входа
def appRemoveTg(request, tg_id):
    TA = TelegramAccount.objects.filter(
        id=tg_id,
        owner=UserData.objects.filter(login=request.user).first()
    )
    if TA:
        for el in TA:
            el.delete()
    return redirect("appSettings")


@csrf_exempt
# @api_view(['POST'])
def tg(request):
    # var data = { 'user': 'myUser', 'pass': 'myPass' };

    # var xhr = new XMLHttpRequest();
    # xhr.open('POST', '/en/app/tg/', true);
    # xhr.setRequestHeader("Content-Type", "application/json; charset=UTF-8");
    # xhr.onreadystatechange = function () {
    #     if (xhr.readyState === 4 && xhr.status === 200) {
    #         var res = JSON.parse(xhr.response);
    #         console.log(res);
    #     }
    # };

    # xhr.send(JSON.stringify(data));
    if request.method == 'POST':
        post_data = json.loads(request.body.decode("utf-8"))
        send_admin_message('qwe')
    return HttpResponse(200)


@api_view(['GET', "POST"])
@__check_auth  # Декоратор проверки авторизации
def appBalance(request, _type=None):
    ud = UserData.objects.filter(login=request.user).first()
    types = request.GET.get("o", 'all')
    type_pay = request.GET.get("t", 'all')
    status = request.GET.get("s", 'all')

    trans = Transactions.objects.filter(from_user=ud)
    data = {
        'app': 'appBalance',
        'cripto': SiteConfiguration.objects.first(),
        'o': types,
        't': type_pay,
        's': status,
        'filter': {
            'type': Transactions.ORDER_TYPE,
            'type_pay': Transactions.ORDER_TYPE_PAY,
            'status': Transactions.ORDER_STATUS,
        },
    }
    if types != 'all':
        # data['make_order'] = True
        trans = trans.filter(type=types)
    if type_pay != 'all':
        # data['make_order'] = True
        trans = trans.filter(type_pay=type_pay)
    if status != 'all':
        # data['make_order'] = True
        item = get_item(Transactions.ORDER_STATUS, status)
        trans = trans.filter(status=status)
    data['transactions'] = trans.order_by('status')
    if request.method == 'POST':
        print('_type', _type)
        data['make_order'] = True
        data['form'] = NewTransfer(request.POST, ud=ud) if _type == 'replenishment' else NewTransfer(ud=ud)
        data['formWithdrawal'] = Withdrawal(request.POST, ud=ud) if _type == 'withdrawal' else NewTransfer(ud=ud)
        tform = None
        if _type == 'withdrawal':
            tform = data['formWithdrawal']
        if _type == 'replenishment':
            tform = data['form']
        dt = {}
        if _type == 'withdrawal':
            if tform.errors:
                for el in tform.errors.get_json_data()['__all__']:
                    dt[el['code']] = el['message']
                setattr(tform, 'error', dt)
        if tform.is_valid():
            return redirect('appBalance', 's')
    else:
        data['form'] = NewTransfer(ud=ud)
        data['formWithdrawal'] = Withdrawal(ud=ud)


    p = getUserData(request, data)

    return render(request,
                  context=p,
                  template_name='app/balance.html')


@api_view(['GET'])
@__check_auth  # Декоратор проверки авторизации
@__check_registers  # Декоратор проверки оплаты входа
def appAccounts(request):
    apikeys = APIKeys.objects.filter(owner__login=request.user).order_by('-status')
    return render(request,
                  context=getUserData(request, {'app': 'appAccounts', 'apikeys': apikeys}),
                  template_name='app/accounts.html')


@api_view(['POST'])
@__check_auth  # Декоратор проверки авторизации
@__check_registers  # Декоратор проверки оплаты входа
def appAccountsSwitchStatus(request, id_key=None):
    apikeys = APIKeys.objects.filter(owner__login=request.user, id=id_key)
    if apikeys:
        apikeys = apikeys[0]
        apikeys.status = not apikeys.status
        apikeys.save()
        return JsonResponse(getResponceApi(request, {'text': l_('Set new status'), 'switch': True}),
                            content_type="application/json", status=200)
    else:
        return JsonResponse(getResponceApi(request, {'text': l_('Not found api key'), 'reload': False}),
                            content_type="application/json", status=404)


@api_view(['GET'])
@__check_auth  # Декоратор проверки авторизации
# @__check_registers  # Декоратор проверки оплаты входа
def appTransactionsSetStatus(request, id, status):
    t = None
    if status == 2:
        t = Transactions.objects.filter(uuid=id.replace('wv_', ''), status=1)
    else:
        t = Transactions.objects.filter(uuid=id.replace('wv_', ''))
    if t:
        t = t[0]
        t.status = int(status)
        t.save()
        send_admin_message(f'Кошелёк {t.wallet}\nОтправил {t.total}', t.uuid)
    return redirect('appBalance', 's')
    # return HttpResponse('ss')


@api_view(['GET'])
@__check_auth  # Декоратор проверки авторизации
@__check_registers  # Декоратор проверки оплаты входа
def appAccountsRemoveKey(request, id_key=0):
    apikey = APIKeys.objects.filter(id=id_key, owner__login=request.user)
    if apikey:
        apikey.first().delete()
    return redirect('appAccounts')


@api_view(['GET', 'POST'])
@__check_auth  # Декоратор проверки авторизации
@__check_registers  # Декоратор проверки оплаты входа
def appAPIKeys(request):
    if request.method == 'POST':
        form = APIKeysForm(request.POST)
        if form.is_valid():
            data = {
                'place': request.POST['place'],
                'title': request.POST['name_integration'],
                'key_public': request.POST['public_key'],
                "key_private": request.POST['private_key'],
            }
            AKeys = APIKeys.objects.filter(**data)
            if AKeys:
                AKeys = AKeys[0]
                AKeys.owner = UserData.objects.filter(login=request.user).first()
                AKeys.owner.api_token.add(AKeys)
                AKeys.owner.save()
                AKeys.save()
            return redirect('appDashboard')
    else:
        form = APIKeysForm()
    return render(request,
                  context=getUserData(request, {'app': 'appAPIKeys', 'form': form}),
                  template_name='app/api-keys.html')


@api_view(['GET', 'POST'])
@__check_auth  # Декоратор проверки авторизации
@__check_registers  # Декоратор проверки оплаты входа
def appTGKeys(request):
    if request.method == 'POST':
        form = TGKeysForm(request.POST)
        if form.is_valid():
            data = {
                'title': request.POST['name_integration'],
                'tg_token': request.POST['tg_key'],
            }
            AKeys = TelegramAccount.objects.filter(**data)
            if AKeys:
                AKeys = AKeys[0]
                # FIXME: овнер должен даваться в боте
                AKeys.owner = UserData.objects.filter(login=request.user)[0]
                AKeys.save()
                a = send_message([data['tg_token']], (f'Ваш телеграмм аккаунт подключен к аккаунту {AKeys.owner.mail}'))
                if not a:
                    AKeys.delete()
            return redirect('appSettings')
    else:
        form = TGKeysForm()
    return render(request,
                  context=getUserData(request, {'app': 'appTGKeys', 'form': form}),
                  template_name='app/tg-keys.html')


@api_view(['GET', 'POST'])
@__check_auth  # Декоратор проверки авторизации
@__check_registers  # Декоратор проверки оплаты входа
def app2FA(request):
    c = UserData.objects.filter(login=request.user).first()
    data = {'app': 'app2FA'}
    if request.method == 'POST':
        form = TwoFactorAuthForm(request.POST, client=c)
        if form.is_valid():
            # data =
            return redirect('appSettings')
        else:
            data['form'] = form
            data['qrcode'] = c.TwoFA
    else:
        form = TwoFactorAuthForm(client=c)
        data['form'] = form
        qr = TwoFactorAuth('LuckyTrade')
        if c.TwoFA:
            if c.TwoFA.verificated:
                c.TwoFA.delete()
                return redirect('appSettings')
            else:
                data['qrcode'] = c.TwoFA
            # data['qrcode'] = c.TwoFA
        else:
            new_qr_secret = qr.create()
            qr_url = qr.getQR(secret=new_qr_secret, issuer=qr.title, account=c.mail)
            img = urlopen(qr_url).read()

            result = urlretrieve(qr_url)  # image_url is a URL to an image
            # self.photo is the ImageField
            new_TwoFA = TwoFA()
            new_TwoFA.qr_url.save(
                new_qr_secret,
                File(open(result[0], 'rb'))
            )
            new_TwoFA.code = new_qr_secret
            new_TwoFA.save()
            data['qrcode'] = new_TwoFA
            c.TwoFA = new_TwoFA
            c.save()

    return render(request,
                  context=getUserData(request, data),
                  template_name='app/2FA.html')


@api_view(['GET', 'POST'])
@__check_auth  # Декоратор проверки авторизации
@__check_registers  # Декоратор проверки оплаты входа
def appPools(request):
    c = UserData.objects.filter(login=request.user)[0]
    pools = Pools.objects.filter(ended=False)
    for el in pools:
        if el.now_total != 0:
            el.percent = el.now_total / (el.max_total / 100)
        else:
            el.percent = 0
        el.percent = str(el.percent).replace(',', '.')
    data = {'app': 'appPools', 'pools': pools}
    return render(request,
                  context=getUserData(request, data),
                  template_name='app/pools.html')


@api_view(['GET', 'POST'])
@__check_auth  # Декоратор проверки авторизации
@__check_registers  # Декоратор проверки оплаты входа
def appPool(request, pool_id=0):
    c = UserData.objects.filter(login=request.user)[0]
    pools = Pools.objects.filter(id=pool_id).prefetch_related('users')
    print(pools)
    if not pools:
        return redirect('appPools')
    for el in pools:
        if el.ended:
            return redirect('appPools')
        if el.now_total != 0:
            el.percent = el.now_total / (el.max_total / 100)
        else:
            el.percent = 0
        el.percent = str(el.percent).replace(',', '.')
        el.logs = PoolLogs.objects.filter(pool=el)
        if el.status and not el.ended:
            print(dt.date.today())
            days = ((el.data_start + dt.timedelta(days=30)) - dt.date.today()).days
            el.count_day_to_end = 0 if days <= 0 else days

        el.date_to_end = PoolLogs.objects.filter(pool=el)
        total_logs = 0
        percent = 0
        for el_l in el.logs:
            total_logs += 1
            percent += ((float(el_l.end_total) - float(el_l.start_total)) / float(el_l.start_total)) * 100
        el.followers = el.users.all()
        try:
            el.percent = percent / total_logs
        except:
            el.percent = 0

    mydata = PoolUsers.objects.filter(pool=pools[0], user=c)
    print(mydata)
    if mydata:
        mydata = mydata[0]
    else:
        mydata = PoolUsers()
        mydata.pool = pools[0]
        mydata.user = c
        mydata.total = 0
        mydata.percent = 0
        mydata.take_money = False
        mydata.save()
    pools[0].users.add(mydata)
    data = {'app': 'appPool', 'pool': pools[0], 'userdata': mydata}
    if request.method == "POST":
        form = SendMoneyToPool(request.POST, ud=c, pool=pools[0])
        data['SendMoneyToPool'] = form
        print(form.is_valid())
        print(form.is_valid())
        if form.is_valid():
            new_TR = Transactions()
            new_TR.data_end = dt.datetime.now()
            new_TR.from_user = UserData.objects.filter(login=request.user)[0]
            new_TR.total = form.data['total']
            new_TR.type = Transactions.ORDER_TYPE[0][0]
            new_TR.descriptions = f"Пополнил баланс '{form.pool.title}' на сумму ({form.data['total']} USD)"
            new_TR.type = Transactions.ORDER_TYPE[2][0]
            new_TR.type_pay = Transactions.ORDER_TYPE_PAY[2][0]
            new_TR.status = Transactions.ORDER_STATUS[4][0]
            new_TR.save()
            return redirect('appPool', pool_id)

    if request.method == "GET":
        form = SendMoneyToPool(ud=c)
        data['SendMoneyToPool'] = form

    return render(request,
                  context=getUserData(request, data),
                  template_name='app/pool.html')


@api_view(['GET', 'POST'])
@__check_auth  # Декоратор проверки авторизации
@__check_registers  # Декоратор проверки оплаты входа
def appPayment(request, _status=None):
    if _status == 'success':
        data = {
            'header': l_('Ваш платеж выполнен'),
            'description': l_('С уважением ваш') + ' Lucky Trade',
        }
    else:
        data = {
            'header': l_('Ваш платеж не выполнен'),
            'description': l_('Наш сервис временно Не принимает платежи') + ' Lucky Trade',
        }
    return render(request,
                  context=getUserData(request, data),
                  template_name='app/payment.html')


@api_view(['GET'])
@__check_auth  # Декоратор проверки авторизации
@__check_registers  # Декоратор проверки оплаты входа
def beginningPayment(request):
    return render(request,
                  context=getUserData(request),
                  template_name='app/welcome-page.html')


@api_view(['GET'])
@__check_auth  # Декоратор проверки авторизации # @__check_registers  # Декоратор проверки оплаты входа
def payments(request):
    distribution_of_money(
        UserData.objects.filter(mail='bar').first(),
        150
    )
    return HttpResponse('good')


@api_view(['GET'])
def recordingLogs(request):
    recording_logs(
        UserData.objects.filter(mail='amal').first(),
        'descriptions',
        150
    )
    return HttpResponse('good')


@api_view(['GET'])
@__check_auth  # Декоратор проверки авторизации # @__check_registers  # Декоратор проверки оплаты входа
def appReferral(request):
    logs = ReferralLogs.objects.filter(user__login=request.user).order_by('-data')
    referral = UserData.objects.filter(login=request.user)[0].referral
    return render(
        request,
        context=getUserData(request, {
            'host': settings.HOST_ADDRESS,
            'referral_data': logs.values(),
            'referral_key': referral,
            'app': 'appReferral'
        }),
        template_name='app/partner.html')

