from django.db import models


class Department(models.Model):
    nick_name = models.TextField(max_length=100, default='')
    name = models.TextField(max_length=100)
    desc = models.TextField()
    question = models.TextField()
    deleted = models.BooleanField(default=False)
    created_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nick_name


class PersonInfo(models.Model):
    name = models.TextField(max_length=100)
    student_id = models.TextField(max_length=100)
    gender = models.TextField(max_length=100)
    grade = models.TextField(max_length=100, default='1')
    major = models.TextField(max_length=100)
    phone_number = models.TextField(max_length=100)
    self_intro = models.TextField(max_length=100)
    question_one = models.TextField(max_length=1000)
    question_two = models.TextField(max_length=1000)
    # TODO: for capability and lazy Patrick
    inclination_one = models.TextField(max_length=100)
    inclination_two = models.TextField(max_length=100)
    department = models.ManyToManyField(Department)

    share_work = models.TextField(max_length=100)
    photo = models.TextField(max_length=100)
    date_time = models.DateTimeField(auto_now_add=True)
    mail_address = models.TextField(default='')

    user_agent = models.TextField(max_length=1000, default='not given')
    time_spend = models.TextField(max_length=100, default='not given')

    inc_one_time = models.TextField(max_length=100, default='0')
    inc_two_time = models.TextField(max_length=100, default='0')
    star_amount = models.IntegerField(default=0)
    is_spam = models.TextField(default='false')
    deleted = models.BooleanField(default=False)
    total_marks = models.FloatField(default=25.0)

    def __str__(self):
        return self.name


class AuthCookie(models.Model):
    cookie_value = models.TextField()
    expire_time = models.IntegerField(default=1)
    is_valid = models.BooleanField(default=True)
    date_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.date_time
