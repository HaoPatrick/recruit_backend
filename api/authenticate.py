from datetime import datetime
from api.models import AuthCookie
from django.core.exceptions import ObjectDoesNotExist


def user_and_password_auth(user, password):
    import os.path
    base = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(base, 'info.txt'), 'r') as f:
        correct_user = f.readline()[:-1]
        correct_pass = f.readline()[:-1]
    if user == correct_user and password == correct_pass:
        return True
    else:
        return False


def generate_cookie():
    import random
    import hashlib
    datetime_now = str(datetime.now())
    encryption_salt = datetime_now + 'qsclove' + str(random.random())
    cookie = hashlib.sha256(encryption_salt.encode('utf-8')).hexdigest()
    return cookie


def auth_cookie(cookie_value):
    try:
        token = AuthCookie.objects.get(cookie_value=cookie_value)
    except ObjectDoesNotExist as e:
        return False
    stored_day = token.date_time.day
    stored_month = token.date_time.month
    current_time = datetime.now()
    if stored_month == current_time.month and stored_day == current_time.day:
        return True
    else:
        return False


def login_required(request):
    try:
        if request.POST.get('cookie'):
            token_valid = auth_cookie(request.POST['cookie'])
            if not token_valid:
                raise CookieError('Invalid token')
        elif request.GET.get('cookie'):
            token_valid = auth_cookie(request.GET['cookie'])
            if not token_valid:
                raise CookieError('Invalid token')
        else:
            raise CookieError('Invalid token')
    except CookieError:
        return False
    return True


class CookieError(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)

