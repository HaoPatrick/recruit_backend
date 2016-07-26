from django.shortcuts import render
from django.http import HttpResponse
from api.models import PersonInfo
from django.core import serializers
from django.views.decorators.csrf import csrf_exempt
from django.utils.datastructures import MultiValueDictKeyError
from api.validators import check_if_spam


# Create your views here.
def test(request):
    return HttpResponse('Test OK')


@csrf_exempt
def save_person_info(request):
    if request.method == 'POST':
        try:
            name = request.POST['name']
            student_id = request.POST['student_id']
            gender = request.POST['gender']
            major = request.POST['major']
            phone_number = request.POST['phone_number']
            self_intro = request.POST['self_intro']
            question_one = request.POST['question_one']
            question_two = request.POST['question_two']
            inclination_one = request.POST['inclination_one']
            inclination_two = request.POST['inclination_two']
            share_work = request.POST['share_work']
            photo = request.POST['photo']
            user_agent = request.POST['user_agent']
            time_spend = request.POST['time_spend']
        except MultiValueDictKeyError:
            return HttpResponse('Errrrrrrrrrrrror 110')
        # TODO: Validate the post data
        data_collection = [
            name, student_id, gender, major, phone_number, self_intro, question_one, question_two,
            inclination_one, inclination_two, share_work, photo, user_agent, time_spend
        ]
        is_spam = False
        PersonInfo.objects.create(
            name=name,
            student_id=student_id,
            gender=gender,
            major=major,
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
        return HttpResponse('OK')
    else:
        return HttpResponse('Error 233')


def get_detailed_person(request):
    if request.method == 'GET':
        query_by_department = []
        query_by_id = []
        query_by_name = []
        query_by_phone = []
        if request.GET.get('department'):
            department = request.GET['department']
            department_persons_one = PersonInfo.objects.filter(inclination_one=department)
            department_persons_two = PersonInfo.objects.filter(inclination_two=department)
            query_by_department = list(department_persons_one) + list(department_persons_two)
        if request.GET.get('student_id'):
            query_by_id = list(PersonInfo.objects.filter(student_id=request.GET['student_id']))
        if request.GET.get('name'):
            query_by_name = list(PersonInfo.objects.filter(name=request.GET['name']))
        if request.GET.get('phone_number'):
            query_by_phone = list(PersonInfo.objects.filter(phone_number=request.GET['phone_number']))
        unique_set = set(query_by_id + query_by_phone + query_by_name + query_by_department)
        json_person = serializers.serialize('json', unique_set)
        return HttpResponse(json_person, content_type='application/json')

    else:
        return HttpResponse('Error 233')


def retrieve_person(request):
    if request.method == 'GET':
        query_start = 0
        query_end = 0
        if request.GET.get('page'):
            page_number = request.GET['page']
            try:
                page_number = int(page_number)-1
            except ValueError:
                return HttpResponse('Erroooooooooor 110')
            all_person = PersonInfo.objects.all()[page_number * 20:page_number + 20]
        else:
            try:
                if request.GET.get('start'):
                    query_start = int(request.GET['start'])
                if request.GET.get('end'):
                    query_end = int(request.GET['end'])
            except ValueError:
                return HttpResponse('Erroooooooooor 110')
            if query_end > query_start >= 0:
                all_person = PersonInfo.objects.all()[query_start:query_end]
            elif query_start != 0 and query_end == 0:
                all_person = PersonInfo.objects.all()[query_start:]
            elif query_end == 0 and query_start == 0:
                all_person = PersonInfo.objects.all()
            else:
                return HttpResponse('Erroooooooooor 110')
        json_person = serializers.serialize('json', all_person)
        return HttpResponse(json_person, content_type='application/json')
