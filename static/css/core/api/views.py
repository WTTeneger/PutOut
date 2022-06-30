import secrets
import string
from itertools import count

import pytz
from loguru import logger
from django.http import HttpResponse
from rest_framework.decorators import api_view

from tg_bot import send_message
from ..app.thirdparty_functions import recording_logs
from ..main.models import *
from ..main.text_to_tg import referral_link_register

# Create your views here.

alphabet = string.ascii_letters + string.digits


def isint(s):
    try:
        int(s)
        return True
    except ValueError:
        return False


def createReferral():
    while True:
        code = ''.join(secrets.choice(alphabet) for i in range(8))
        if not Referral.objects.filter(referral_code=code):
            break

    new_referral = Referral()
    new_referral.referral_code = code
    new_referral.count_friends = 0
    new_referral.save()
    return new_referral


def createUser(data):
    user = User.objects.create_user(username=data['email'],
                                    email='',
                                    password=data['password1'])
    return user


def createUserData(data):
    new_user_data = UserData()
    new_user_data.login = createUser(data)
    new_user_data.mail = data['email']
    new_user_data.username = data['email']
    new_user_data.account_type = 'client'
    new_user_data.referral = createReferral()
    new_user_data.save()
    referal_users = []
    if 'referral_key' in data:
        from_user_data_line_1 = UserData.objects.filter(referral__referral_code=data['referral_key'])
        if from_user_data_line_1:  # Если есть пользователь с твои реф ключём даём ему тебя в 1 линию
            from_user_data_line_1 = from_user_data_line_1[0]
            new_user_data.from_user = from_user_data_line_1
            from_user_data_line_1.referral.line_1.add(new_user_data)
            from_user_data_line_1.referral.count_friends = int(from_user_data_line_1.referral.count_friends)+1
            from_user_data_line_1.referral.save()
            from_user_data_line_1.save()
            referal_users.append(from_user_data_line_1)
            if from_user_data_line_1.from_user:  # Если есть пользователь у того кто позвал тебя даём ему тебя в 2 линию
                from_user_data_line_2 = from_user_data_line_1.from_user
                from_user_data_line_2.referral.line_2.add(new_user_data)
                from_user_data_line_2.save()
                referal_users.append(from_user_data_line_2)
                if from_user_data_line_2.from_user:  # Если есть пользователь у этого даём ему тебя в 3 линию
                    from_user_data_line_3 = from_user_data_line_2.from_user
                    from_user_data_line_3.referral.line_3.add(new_user_data)
                    from_user_data_line_3.save()
                    referal_users.append(from_user_data_line_3)

    for num, el in enumerate(referal_users):
        for token in TelegramAccount.objects.filter(owner=el):
            send_message([token.tg_token], (l_(referral_link_register.format(num + 1))))
    new_user_data.save()
    recording_logs(
        new_user_data,
        l_('Зарегистрировался в проекте'),
        '0'
    )
    return new_user_data


"""
REQ_P < QueryDict: {'date': ['2022-06-30T00:00:00+03:00'], 'order_id': ['1'], 'order_num': ['test'],
                    'domain': ['luckytrade.payform.ru'], 'sum': ['1000.00'], 'customer_phone': ['+79999999999'],
                    'customer_email': ['email@domain.com'], 'customer_extra': ['тест'],
                    'payment_type': ['Пластиковая карта Visa, MasterCard, МИР'], 'commission': ['3.5'],
                    'commission_sum': ['35.00'], 'attempt': ['1'], 'sys': ['test'],
                    'products[0][name]': ['Доступ к обучающим материалам'], 'products[0][price]': ['1000.00'],
                    'products[0][quantity]': ['1'], 'products[0][sum]': ['1000.00'], 'payment_status': ['success'],
                    'payment_status_description': ['Успешная оплата']} >
"""


@api_view(['GET', "POST"])
def apiCallback(request):
    if request.method == 'POST':
        logger.info(f'REQ_P {request.POST} header{request.headers}')
        _sign = request.headers.get('Sign', None)
        if not _sign:
            return HttpResponse("Did not receive or incorrect Sign", 405)
        data = request.POST.get('date', None)
        order_num = request.POST.get('order_num', None)
        sum = request.POST.get('sum', None)
        print('sum', sum)
        status = request.POST.get('payment_status', None)
        descriptions = request.POST.get('payment_status_description', None)
        if status != 'success':
            print("Not success")
            return HttpResponse("Not success", status=500)

        try:
            dt_order = datetime.datetime.strptime(data, "%Y-%m-%dT%H:%M:%S%z")
            dt_now_minus_hours = datetime.datetime.now(dt_order.tzinfo) - datetime.timedelta(hours=2)
            print(dt_order)
            print(dt_now_minus_hours)
            if not data or not dt_order or dt_order < dt_now_minus_hours:
                print("Not correct data 1")
                return HttpResponse("Not correct data", status=500)
        except:
            print("Not correct data 2")
            return HttpResponse("Not correct data", status=500)
        user_id = None
        transaction_id = order_num
        if '_' in order_num:
            [user_id, transaction_id] = order_num.split('_')
        try:
            if user_id:
                transaction = Transactions.objects.filter(uuid=transaction_id, from_user__id=user_id) \
                    .prefetch_related('from_user')
            else:
                transaction = Transactions.objects.filter(uuid=transaction_id) \
                    .prefetch_related('from_user')
        except:
            print("is not a valid UUID.")
            return HttpResponse("is not a valid UUID.", status=500)

        if not transaction:
            print("We don't have a transaction with this UUID")
            return HttpResponse("We don't have a transaction with this UUID", status=404)

        transaction = transaction[0]
        if transaction.status in ['3', '4', '5']:
            print('The status of this transaction is already finished"')
            return HttpResponse("The status of this transaction is already finished", status=400)
        try:
            sum = sum.split('.')[0]
        except:
            print("Sum not split")
            return HttpResponse("Sum not split", status=500)
        if not isint(sum):
            print("Sum cant int")
            return HttpResponse("Sum cant int", status=500)

        transaction.data_end = datetime.datetime.now()
        sm = int(sum) / 50
        transaction.descriptions = f'Успешно пополнил баланс на сумму {sm}$'
        transaction.total = sm
        transaction.status = 5
        transaction.save()
        user = transaction.from_user
        if not user.verified:
            if sm >= 150:
                user.verified = True
                user.free_sub = True
        user.balance += sm
        user.save()





        return HttpResponse(f'_status - {request.POST}', status=200)
    if request.method == 'GET':
        logger.info(f'REQ_G {request.GET}  header{request.headers}')
        return HttpResponse(f'_status - {request.GET}', status=200)
