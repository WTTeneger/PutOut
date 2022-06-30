import requests


class Payment:
    payment = None
    url = 'https://luckytrade.payform.ru/?'
    secret = 'd55adae5108684fbc28a1de3a26fc35af3a03a66aaf478aaa909cb995f2969c7'

    def __new__(cls, *args, **kwargs):
        # Блочит повторное создание QR генераторов
        if Payment.payment:
            return Payment.payment
        else:
            return super().__new__(cls)

    def __init__(self):
        payment = self

    def create_url(self, order_id, total, customer_phone, customer_email, demo_mode=False):
        data = {
            'order_id': order_id,
            'customer_phone': customer_phone,
            'customer_email': customer_email,
            'customer_extra': f'Пополнение балланса LuckyTrader на сумму {total}',
            'do': 'pay'
        }
        product = f'products[0][price]={total}&' \
                  f'products[0][quantity]=1&' \
                  f'products[0][name]=Пополнение балланса LuckyTrader на сумму {total}'
        url = self.url
        for el in data:
            txt = f'{el}={data[el]}&'
            print('txt', txt)
            url += txt
        # url.replace(' ', '%20')
        # if url[-1] == '?':
        #     url = url[:len(url) - 1]
        return url + product + '&demo_mode=1' if demo_mode else url + product


# url = Payment().create_url(12, 221, '79628855545', 'amal.agishev@mail.ru')
# print(url)
"""
https://luckytrade.payform.ru/?order_id=test&customer_phone=79998887755&products[0][price]=2000&products[0][quantity]=1&products[0][name]=Обучающие%20материалы&customer_extra=Полная%20оплата%20курса&do=pay
https://luckytrade.payform.ru/?order_id=12&customer_phone=79999999999&customer_email=amal.agishev@mail.ru&customer_extra=Пополнение балланса LuckyTrader на сумму 221&do=pay&products[0][price]=221&products[0][quantity]=1&products[0][name]=Пополнение балланса LuckyTrader на сумму 221
"""

"""
{'date': ['2022-06-30T16:08:01+03:00'], 'order_id': ['4476470'], 'order_num': ['20_055c08c5-f9b0-4584-9e5f-34da22ee1de9'], 'domain': ['luckytrade.payform.ru'], 'sum': ['50.00'], 'customer_phone': ['+79999999999'], 'customer_email': ['amal.agishev@mail.ru'], 'customer_extra': ['Пополнение балланса LuckyTrader на сумму 50'], 'payment_type': ['Оплата картой, выпущенной в РФ'], 'commission': ['3.5'], 'commission_sum': ['1.75'], 'attempt': ['4'], 'products[0][name]': ['Пополнение балланса LuckyTrader на сумму 50'], 'products[0][price]': ['50.00'], 'products[0][quantity]': ['1'], 'products[0][sum]': ['50.00'], 'payment_status': ['success'], 'payment_status_description': ['Успешная оплата'], 'payment_init': ['manual']}> header{'Content-Length': '1059', 'Content-Type': 'application/x-www-form-urlencoded', 'Host': '31.31.196.26:8001', 'User-Agent': 'curl', 'Accept': '*/*', 'Sign': '7ecddd19357698ff17542a31250a4b09436fe21ba5963b30647087c143de81d9'}
"""
