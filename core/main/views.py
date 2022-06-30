import random
# from datetime import datetime, timedelta

from django import forms
from django.conf import settings
from django.contrib.auth import login, logout
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.core.validators import validate_email
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.template.loader import render_to_string
from django.utils import translation
from django.utils.translation import gettext_lazy as _
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from ..utils.utils import __check_auth, __check_registers
from .models import *


def index(request):
    return render(request, 'main/index.html', {'languages': settings.LANGUAGES})
