from api.models import PersonInfo
from django.core import serializers
from django.http import HttpResponse
from django.db.models import Q


def detail_person_exclude_query(request):
    total_person = PersonInfo.objects.filter(deleted=False)
    if request.GET.get('department'):
        department = request.GET['department']
        total_person = total_person.filter(Q(inclination_one=department) | Q(inclination_two=department))
    if request.GET.get('student_id'):
        total_person = total_person.filter(student_id=request.GET['student_id'])
    if request.GET.get('name'):
        total_person = total_person.filter(name=request.GET['name'])
    if request.GET.get('phone_number'):
        total_person = total_person.filter(phone_number=request.GET['phone_number'])
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
    json_person = serializers.serialize('json', total_person)
    return json_person


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
    unique_set = set(query_by_id + query_by_phone + query_by_name + query_by_department)
    json_person = serializers.serialize('json', unique_set)
    return json_person
