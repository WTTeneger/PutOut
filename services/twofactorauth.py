#
# url = "https://google-authenticator.p.rapidapi.com/new_v2/"
#
# headers = {
# 	"X-RapidAPI-Host": "google-authenticator.p.rapidapi.com",
# 	"X-RapidAPI-Key": "2511e25f69msh5bea61e277c1b33p13fff6jsn2385749e70c3"
# }
#
# response = requests.request("GET", url, headers=headers)
#
# print(response.text)
import requests

x_key = '2511e25f69msh5bea61e277c1b33p13fff6jsn2385749e70c3'


class TwoFactorAuth:
    QR_Before = None
    methods = {
        'create': {'url': "https://google-authenticator.p.rapidapi.com/new_v2/", 'method': "GET", 'private': True},
        'getQR': {'url': "https://google-authenticator.p.rapidapi.com/enroll/", 'method': "GET", 'private': True,
                  'atr': ["secret", "issuer", "account"]},
        'validate': {'url': "https://google-authenticator.p.rapidapi.com/validate/", 'method': "GET", 'private': True,
                     'atr': ["secret", "code"]},
    }

    def __new__(cls, *args, **kwargs):
        # Блочит повторное создание QR генераторов
        if TwoFactorAuth.QR_Before:
            return TwoFactorAuth.QR_Before
        else:
            return super().__new__(cls)


    def __init__(self, _title='Default'):
        self.t = 0
        self.APIKey = x_key
        self.title = _title
        self.headers = {
            "X-RapidAPI-Host": "google-authenticator.p.rapidapi.com",
            "X-RapidAPI-Key": x_key
        }
        TwoFactorAuth.QR_Before = self

    def __getattr__(self, name):
        def wrapper(*args, **kwargs):
            kwargs.update(command=name)
            return self.call_api(**kwargs)

        return wrapper

    def call_api(self, **kwargs):
        command = self.methods[kwargs.pop('command')]
        payload = kwargs

        def sublist_in_list(listMain, listD):
            for el in listD:
                if el not in listMain:
                    return False
            return True

        if 'atr' in command:
            if sublist_in_list(payload, command['atr']):
                response = requests.request(command['method'], command['url'], headers=self.headers, params=payload)
                return response.text
            else:
                assert False, 'Вы передали не все параметры'
        else:
            response = requests.request(command['method'], command['url'], headers=self.headers, params=payload)
            return response.text
            # return 'Вы передали не все параметры'


# qr1 = QRCode('2511e25f69msh5bea61e277c1b33p13fff6jsn2385749e70c3', 'LuckyTrade')
# qr2 = QRCode('2511e25f69msh5bea61e277c1b33p13fff6jsn2385749e70c3', 'LuckyTrade')
# code = qr1.create()
# print(code)
