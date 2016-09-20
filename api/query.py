from api.models import PersonInfo, Department
from django.core import serializers
from django.db.models import Q
from django.core.exceptions import ObjectDoesNotExist
from django.utils.datastructures import MultiValueDictKeyError
import json


# TODO: Warning, no test below!!!
def detail_person_exclude_query(request):
    total_person = PersonInfo.objects.filter(deleted=False)
    if request.GET.get('department'):
        department = request.GET['department']
        total_person = total_person.filter(Q(inclination_one=department) | Q(inclination_two=department))
    if request.GET.get('student_id'):
        total_person = total_person.filter(student_id__contains=request.GET['student_id'])
    if request.GET.get('name'):
        total_person = total_person.filter(name__contains=request.GET['name'])
    if request.GET.get('phone_number'):
        total_person = total_person.filter(phone_number__contains=request.GET['phone_number'])
    if request.GET.get('gender'):
        total_person = total_person.filter(gender=request.GET['gender'])
    if request.GET.get('grade'):
        total_person = total_person.filter(grade=request.GET['grade'])
    if request.GET.get('linux'):
        total_person = total_person.filter(user_agent__contains='Linux')
    if request.GET.get('chrome'):
        total_person = total_person.filter(user_agent__contains='Chrome')
    if request.GET.get('windows'):
        total_person = total_person.filter(user_agent__contains='Windows')
    if request.GET.get('mac'):
        total_person = total_person.filter(user_agent__contains='Mac')
    if request.GET.get('ie'):
        total_person = total_person.filter(Q(user_agent__contains='MSIE') | Q(user_agent='360SE'))
    if request.GET.get('edge'):
        total_person = total_person.filter(user_agent__contains='Edge')
    list_response = []
    dict_response = []
    for index, person in enumerate(total_person):
        if person.student_id in dict_response:
            continue
        else:
            dict_response.append(person.student_id)
        list_response.append({
            'pk': person.pk,
            'model': person._meta.model_name,
            'fields': {
                'name': person.name,
                'gender': person.gender,
                'student_id': person.student_id,
                'inclination_one': person.inclination_one,
                'inclination_two': person.inclination_two,
                'major': person.major,
                'phone_number': person.phone_number
            }
        })
    json_person = json.dumps(list_response)
    return json_person


# Not implemented!
def detail_person_combine_query(request):
    query_by_department = []
    query_by_id = []
    query_by_name = []
    query_by_phone = []
    if request.GET.get('department'):
        department = request.GET['department']
        department_persons_one = PersonInfo.objects.filter(inclination_one=department).exclude(deleted=True)
        department_persons_two = PersonInfo.objects.filter(inclination_two=department).exclude(deleted=True)
        query_by_department = list(department_persons_one) + list(department_persons_two)
    if request.GET.get('student_id'):
        query_by_id = list(
            PersonInfo.objects.filter(student_id=request.GET['student_id']).exclude(deleted=True))
    if request.GET.get('name'):
        query_by_name = list(PersonInfo.objects.filter(name=request.GET['name']).exclude(deleted=True))
    if request.GET.get('phone_number'):
        query_by_phone = list(PersonInfo.objects.filter(
            phone_number=request.GET['phone_number']).exclude(deleted=True))
    unique_set = list(set(query_by_id + query_by_phone + query_by_name + query_by_department))
    json_person = serializers.serialize('json', unique_set)
    return json_person


def print_specific_department(request):
    try:
        department = request.GET['department']
    except MultiValueDictKeyError:
        return False
    total_person = PersonInfo.objects.exclude(deleted=True).filter(
        Q(inclination_one=department) | Q(inclination_two=department))
    if request.GET.get('count'):
        print_count = int(request.GET['count'])
        total_person = total_person.order_by('-pk')[:print_count]
    persons = []
    for person in total_person:
        persons.append(person)
    persons.reverse()
    json_response = serializers.serialize('json', persons)
    return json_response


def recalculate_average_marks(person):
    all_assessment = person.assessment_set.all().filter(deleted=False)
    all_pro_rate = [pro.profession_rate for pro in all_assessment]
    all_coop_rate = [coop.cooperation_rate for coop in all_assessment]
    all_general_rate = [general.general_rate for general in all_assessment]
    all_express = [express.expression_ability for express in all_assessment]
    all_interest = [interest.interesting for interest in all_assessment]

    try:
        average_express = sum(all_express) / float(len(all_express))
        average_interest = sum(all_interest) / float(len(all_interest))
        average_pro = sum(all_pro_rate) / float(len(all_pro_rate))
        average_general = sum(all_general_rate) / float(len(all_general_rate))
        average_cooper = sum(all_coop_rate) / float(len(all_coop_rate))
        total_marks = average_express + average_pro + average_general + average_interest + average_cooper
        all_assessment.update(average_pro=average_pro,
                              average_general=average_general,
                              average_cooper=average_cooper,
                              average_expression=average_express,
                              average_interesting=average_interest)
        person.total_marks = total_marks
        person.save()
    except ZeroDivisionError:
        return


def save_a_person_to_database(request):
    try:
        name = request.POST['name']
        student_id = request.POST['student_id']
        gender = request.POST['gender']
        major = request.POST['major']
        grade = request.POST['grade']
        phone_number = str(int(request.POST['phone_number']))
        self_intro = request.POST['self_intro']
        question_one = request.POST['question_one']
        question_two = request.POST['question_two']
        inclination_one = request.POST['inclination_one']
        inclination_two = request.POST['inclination_two']
        department_one = Department.objects.get(name=inclination_one)
        department_two = Department.objects.get(name=inclination_two)
        share_work = request.POST['share_work']
        photo = request.POST['photo']
        mail_address = request.POST['mail']
        if not validate_email_address(mail_address):
            raise EmailError('Invalid Email')
        user_agent = request.POST['user_agent']
        time_spend = int(int(request.POST['time_spend']) / 1000)
    except MultiValueDictKeyError:
        return False
    except ObjectDoesNotExist:
        return False
    except ValueError:
        return False
    except EmailError:
        return False
    # TODO: Validate the post data
    # purify html
    self_intro = self_intro.replace('(', 'a').replace(')', 'b').replace('on', 'hhh')
    question_one = question_one.replace('(', 'a').replace(')', 'b').replace('on', 'hhh')
    question_two = question_two.replace('(', 'a').replace(')', 'b').replace('on', 'hhh')

    time_min = int(time_spend / 60)
    time_sec = time_spend - time_min * 60
    time_spend = str(time_min) + ' min ' + str(time_sec) + ' s'
    is_spam = False
    person = PersonInfo.objects.create(
        name=name,
        student_id=student_id,
        gender=gender,
        major=major,
        grade=grade,
        mail_address=mail_address,
        phone_number=phone_number,
        self_intro=self_intro,
        question_one=question_one,
        question_two=question_two,
        inclination_one=inclination_one,
        inclination_two=inclination_two,
        share_work=share_work,
        photo=photo,
        user_agent=user_agent,
        time_spend=time_spend,
        is_spam=str(is_spam)
    )
    person.department.add(department_one, department_two)
    from django.conf import settings
    if not settings.TESTING:
        send_email(mail_address, name, student_id, phone_number, inclination_one, inclination_two)
        send_sms(phone_number, name)
    else:
        print('test so skip the email')
    return True


def get_stats_via_department():
    all_department = Department.objects.all()
    stats_list = []
    for depart in all_department:
        stats_list.append(
            {'name': depart.name,
             'count': depart.personinfo_set.count()})
    json_response = json.dumps(stats_list)
    return json_response


def get_department_info(request):
    try:
        if request.GET.get('name'):
            name = request.GET['name']
            target_depart = Department.objects.filter(name=name).filter(deleted=False)
        else:
            target_depart = Department.objects.all().filter(deleted=False)
    except ObjectDoesNotExist:
        return False
    result_list = []
    for depart in target_depart:
        result_list.append({
            'name': depart.name,
            'nick_name': depart.nick_name,
            'desc': depart.desc,
            'question': depart.question,
            'deleted': False,
            'count': depart.personinfo_set.values_list('student_id', flat=True).distinct().count()
        })
    json_response = json.dumps(result_list)
    return json_response


# TODO: Temporary filter, correct version was commented
def get_ranked_person_via_department(request):
    try:
        department_name = request.GET['depart']
        department = Department.objects.get(name=department_name)
    except MultiValueDictKeyError:
        return False
    except ObjectDoesNotExist:
        return False
    all_person = PersonInfo.objects.filter(
        Q(inclination_one=department_name) | Q(inclination_two=department_name)
    ).order_by('-total_marks')
    # all_person = department.personinfo_set.all().order_by('-total_marks')
    json_response = serializers.serialize('json', all_person)
    return json_response


def validate_email_address(email):
    from email.utils import parseaddr
    return '@' in parseaddr(email)[1]


def send_sms(phone_number, name):
    import requests
    url = 'https://sms.yunpian.com/v1/sms/send.json'
    api_key = 'd0d4d333ccb057612c0325521b9403ed'
    msg = '【求是潮】' + name + '同学您好，您的纳新报名表已上传。如需修改，可重新提交。我们将在之后通过短信与您联系，请留意。期待您的加入！'
    params = {'apikey': api_key,
              'mobile': phone_number,
              'text': msg}
    requests.post(url, files={}, data=params)


def send_email(mail_address, name, stu_id, phone_number, inc_one, inc_two):
    import requests
    import random
    import os.path
    base = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(base, 'info.txt'), 'r') as fp:
        lines = fp.readlines()
        api_user = [lines[2][:-1], lines[3][:-1]]
        api_key = lines[4]
    message = "<p>亲爱的" + name + "您好:</p>"
    message += "<p>我们已经收到了您的报名表，请核对下列信息是否准确，重新提交报名表可修改信息（http://joinus.zjuqsc.com)</p>"
    message += "<p>您的学号：" + stu_id + "<br>您的手机号：" + phone_number + \
               "<br>您的第一志愿：" + inc_one + "<br>您的第二志愿：" + inc_two + \
               "<br><br>我们将在之后通过短信通知您具体的面试信息，敬请留意。感谢您报名2016求是潮秋季纳新，期待您的加入！"
    url = "http://sendcloud.sohu.com/webapi/mail.send.json"
    params = {"api_user": api_user[random.randrange(2)],
              "api_key": api_key,
              "from": "tech@zjuqsc.com",
              "to": mail_address,
              "fromname": "求是潮",
              "subject": "感谢报名求是潮",
              "html": message,
              "resp_email_id": "true",
              }
    r = requests.post(url, files={}, data=params)
    print(r.content.decode('utf-8'))


class EmailError(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)
