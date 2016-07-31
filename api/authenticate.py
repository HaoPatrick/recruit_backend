def user_and_password_auth(user, password):
    import os.path
    base = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(base, 'info.txt'), 'r') as f:
        correct_user = f.readline()[:-1]
        correct_pass = f.readline()
    print(correct_user + user+'\n')
    print(correct_pass+password)
    if user == correct_user and password == correct_pass:
        return True
    else:
        return False


def generate_cookie():
    from datetime import datetime
    import random
    import hashlib
    datetime_now = str(datetime.now())
    encryption_salt = datetime_now + 'qsclove' + str(random.random())
    cookie = hashlib.sha256(encryption_salt.encode('utf-8')).hexdigest()
    return cookie
