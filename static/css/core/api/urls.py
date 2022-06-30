from django.urls import path
from . import views
# import threading


urlpatterns = [
    path('v2/callback/', views.apiCallback),
    # path('account/register/', views.accountRegister),
]
