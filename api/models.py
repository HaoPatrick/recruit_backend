from django.db import models


# Create your models here.
class PersonInfo(models.Model):
    name = models.TextField(max_length=100)
    student_id = models.TextField(max_length=100)
    gender = models.TextField(max_length=100)
    major = models.TextField(max_length=100)
    phone_number = models.TextField(max_length=100)
    self_intro = models.TextField(max_length=100)
    question_one = models.TextField(max_length=1000)
    question_two = models.TextField(max_length=1000)
    inclination_one = models.TextField(max_length=100)
    inclination_two = models.TextField(max_length=100)
    share_work = models.TextField(max_length=100)
    photo = models.TextField(max_length=100)
    date_time = models.DateTimeField(auto_now_add=True)

    user_agent = models.TextField(max_length=1000, default='not given')
    time_spend = models.TextField(max_length=100, default='not given')
    is_spam = models.TextField(max_length=100, default='false')

    def __str__(self):
        return self.name
