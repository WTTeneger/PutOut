from django.contrib.auth import logout

# from core.main.models import UserData
from django.shortcuts import redirect


def __check_auth(function_to_decorate):
    """Проверка аунтификации пользователя"""
    def a_wrapper_accepting_arguments(request, *args, **kwargs):
        if request.user.is_authenticated:
            return function_to_decorate(request, *args, **kwargs)
        else:
            return redirect('sign-in')
    return a_wrapper_accepting_arguments


def __apikeys(function_to_decorate):
    """Проверка аунтификации пользователя"""
    def a_wrapper_accepting_arguments(request, *args, **kwargs):
        UserData = []
        user = UserData.objects.filter(login=request.user)
        if user:
            user = user[0]
            if user.api_token.filter(status=True):
                return function_to_decorate(request, *args, **kwargs)
            else:
                return redirect('appDashboard')
        else:
            logout(request)
        return redirect('sign-in')
    return a_wrapper_accepting_arguments


def __check_registers(function_to_decorate):
    """Проверка регистрации(покупки доступа) пользователя"""
    def a_wrapper_accepting_arguments(request, *args, **kwargs):
        # if request.user.is_authenticated:
        user = UserData.objects.filter(login=request.user)
        if user.exists() and not user.first().verified:  # Если пользователь есть и он не оплатил акк
            return redirect('appBalance', 's')
        return function_to_decorate(request, *args, **kwargs)

        # else:
        #     return redirect('sign-in')
    return a_wrapper_accepting_arguments


# def check_correct_password(password):
#     """Проверка пароля на сложность"""
#     # if policy.test(password):
#     #     return 'Password'
#     # if PasswordStats(password).strength() < 0.3:
#     #     return 'Strength'
#     # return None

#     # Если не достаточно разнообразный
#     if PasswordStats(password).strength() < 0.3:
#         raise ValidationError(_('Come up with a more complex password'))
#     # Если неправильный пароль
#     elif policy.test(password):
#         raise ValidationError(
#             _('The password must be longer than 8 characters and contain at least one capital letter, a number and a special character'))
