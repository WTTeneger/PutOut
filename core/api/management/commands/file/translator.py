import os

import polib
import requests

import translater
from lt import settings


class bcolors:
    HEADER = '\033[95m'
    STANDART = '\033[37m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


class Translator:
    folder_id = None
    headers = None
    OAuth = None
    objects = []

    def __init__(self, folder_id, OAuth):
        self.folder_id = folder_id
        self.OAuth = OAuth
        self.IAM_TOKEN = self.IAMToken()
        self.headers = {
            "Content-Type": "application/json",
            "Authorization": "Bearer {0}".format(self.IAM_TOKEN)
        }

    def IAMToken(self):
        data = {'yandexPassportOauthToken': self.OAuth}
        response = requests.post('https://iam.api.cloud.yandex.net/iam/v1/tokens',
                                 json=data)
        if response.status_code == 200:
            return response.json()['iamToken']
        else:
            print("Не удалось получить IAM Keys")

    def translate_to_language(self, texts=None, target_language='ru'):
        body = {
            "targetLanguageCode": target_language,
            "texts": texts,
            "folderId": self.folder_id,
        }

        response = requests.post('https://translate.api.cloud.yandex.net/translate/v2/translate',
                                 json=body,
                                 headers=self.headers
                                 )
        try:
            words = [el['text'] for el in response.json()['translations']]
            return words
        except:
            pass


def translate_po(language='all'):
    l = []
    if language == 'all':
        l = [el[0] for el in settings.LANGUAGES]
    else:
        l = [language]
    for el in l:
        os.system(f'python .\manage.py makemessages -l {el}')
        translator = translater.Translator(settings.YT_folder_id, settings.YT_OAuth)

        po = polib.pofile(f'locale/{el}/LC_MESSAGES/django.po')

        valid_entries = [e for e in po if e.msgstr == '']
        valid_entries_to_translator = [e.msgid for e in valid_entries]
        print(valid_entries)
        print(valid_entries_to_translator)
        if valid_entries_to_translator:
            trans_words = translator.translate_to_language(valid_entries_to_translator, el)
            for num, entry in enumerate(valid_entries):
                # po.append(entry)
                entry.msgstr = trans_words[num]
            po.save()
        print(f"{bcolors.OKGREEN}{el} - готов")
        os.system(f'python .\manage.py compilemessages -l {el}')
        print(f"{bcolors.STANDART}")
    os.system(f'python .\manage.py compilemessages')
    print(f"{bcolors.OKBLUE}all file translated")
    print(f"{bcolors.STANDART}")
