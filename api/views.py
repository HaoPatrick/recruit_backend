from django.http import HttpResponse
from api.models import PersonInfo, Assessment, AuthCookie, Department
from django.core import serializers
from django.views.decorators.csrf import csrf_exempt
from django.utils.datastructures import MultiValueDictKeyError
from django.core.exceptions import ObjectDoesNotExist
from api.authenticate import user_and_password_auth
from api.authenticate import generate_cookie
from api.authenticate import login_required
import json


# Create your views here.
def test(request):
    return HttpResponse('Test OK')


@csrf_exempt
def authentication(request):
    if request.method == 'POST':
        try:
            user_name = request.POST['user_name']
            pass_word = request.POST['pass_word']
            if_correct = user_and_password_auth(user=user_name, password=pass_word)
            if if_correct:
                response_cookie = generate_cookie()
                AuthCookie.objects.create(cookie_value=response_cookie)
                json_response = json.dumps([{'login': 'OK', 'response_token': response_cookie}])
                return HttpResponse(json_response, content_type='application/json')
            else:
                return HttpResponse('Authenticate failed')
        except MultiValueDictKeyError:
            return HttpResponse('Authenticate failed')
        except Exception as e:
            return HttpResponse(e)
    else:
        return HttpResponse('Bad boy...')


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
            time_spend = int(int(request.POST['time_spend']) / 1000)
        except MultiValueDictKeyError:
            return HttpResponse('Errrrrrrrrrrrror 110')
        except Exception as e:
            return HttpResponse('Errrrrrrrrrrrror 110' + str(e))
        # TODO: Validate the post data
        time_min = int(time_spend / 60)
        time_sec = time_spend - time_min * 60
        time_spend = str(time_min) + ' min ' + str(time_sec) + ' s'
        is_spam = False
        try:
            person = PersonInfo.objects.get(student_id=student_id)
            person.name = name
            person.gender = gender
            person.major = major
            person.phone_number = phone_number
            person.self_intro = self_intro
            person.question_one = question_one
            person.inclination_one = inclination_one
            person.inclination_two = inclination_two
            person.photo = photo
            person.share_work = share_work
            person.time_spend += time_spend
            person.save()
        except ObjectDoesNotExist:
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
    if not login_required(request):
        return HttpResponse('Authenticate error')
    if request.method == 'GET':
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
            query_by_id = list(PersonInfo.objects.filter(student_id=request.GET['student_id']).exclude(deleted=True))
        if request.GET.get('name'):
            query_by_name = list(PersonInfo.objects.filter(name=request.GET['name']).exclude(deleted=True))
        if request.GET.get('phone_number'):
            query_by_phone = list(PersonInfo.objects.filter(
                phone_number=request.GET['phone_number']).exclude(deleted=True))
        unique_set = set(query_by_id + query_by_phone + query_by_name + query_by_department)
        json_person = serializers.serialize('json', unique_set)
        return HttpResponse(json_person, content_type='application/json')

    else:
        return HttpResponse('Error 233')


def retrieve_person(request):
    if not login_required(request):
        return HttpResponse('Authenticate error')
    if request.method == 'GET':
        query_start = 0
        query_end = 0
        if request.GET.get('page'):
            page_number = request.GET['page']
            try:
                page_number = int(page_number) - 1
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
        json_person = serializers.serialize('json', all_person.exclude(deleted=True))
        return HttpResponse(json_person, content_type='application/json')


@csrf_exempt
def manage_each_person(request):
    if not login_required(request):
        return HttpResponse('Authenticate error')
    if request.method == 'POST':
        inclination_one_time = ''
        inclination_two_time = ''
        if_star = 0
        try:
            student_id = request.POST['student_id']
            if request.POST.get('inc_one'):
                inclination_one_time = request.POST['inc_one']
            elif request.POST.get('inc_two'):
                inclination_two_time = request.POST['inc_two']
            if request.POST.get('star'):
                if_star = int(request.POST['star'])
            person = PersonInfo.objects.filter(student_id=student_id)[0]
        except MultiValueDictKeyError:
            return HttpResponse('Errrrrrrrrrrrrrrrrrror 110')
        except IndexError:
            return HttpResponse('Error 233')
        # TODO: simple validate
        if if_star == 1:
            person.star_amount += 1
        elif if_star == 2:
            person.star_amount -= 1
        if inclination_one_time:
            person.inc_one_time = inclination_one_time
        if inclination_two_time:
            person.inc_two_time = inclination_two_time
        person.save()
        return HttpResponse('OK')

    return HttpResponse('Oh my bad guy')


@csrf_exempt
def department_info(request):
    if request.method == 'POST':
        if not login_required(request):
            return HttpResponse('Authenticate error')
        try:
            nick_name = request.POST['niname']
            name = request.POST['name']
            desc = request.POST['desc']
            question = request.POST['ques']
        except MultiValueDictKeyError:
            return HttpResponse('Error 110')
        try:
            target = Department.objects.get(nick_name=nick_name)
        except ObjectDoesNotExist:
            target = Department.objects.create(
                name=name,
                desc=desc,
                question=question,
                nick_name=nick_name
            )
        target.name = name
        target.desc = desc
        target.question = question
        target.save()
        return HttpResponse('OK')
    elif request.method == 'GET':
        try:
            name = request.GET['name']
            target_depart = Department.objects.filter(name=name).filter(deleted=False)
        except MultiValueDictKeyError:
            target_depart = Department.objects.all().filter(deleted=False)
        except ObjectDoesNotExist:
            return HttpResponse('Does not exist')
        json_depart = serializers.serialize('json', target_depart)
        return HttpResponse(json_depart, content_type='application/json')


@csrf_exempt
def delete_item(request):
    if not login_required(request):
        return HttpResponse('Authenticate error')
    if request.method == 'POST':
        if request.POST.get('nick_name'):
            nick_name = request.POST['nick_name']
            recover_signal = request.POST['recover']
            try:
                department = Department.objects.get(nick_name=nick_name)
            except ObjectDoesNotExist:
                return HttpResponse('Does not exist')
            if recover_signal == '1':
                department.deleted = False
            else:
                department.deleted = True
            department.save()
        if request.POST.get('student_id'):
            student_id = request.POST['student_id']
            recover_signal = request.POST['recover']
            try:
                student = PersonInfo.objects.get(student_id=student_id)
            except ObjectDoesNotExist:
                return HttpResponse('Does not exist')
            if recover_signal == '1':
                student.deleted = False
            else:
                student.deleted = True
            student.save()
        return HttpResponse('OK')


def recycle(request):
    if request.method == 'GET':
        person = list(PersonInfo.objects.filter(deleted=True))
        department = list(Department.objects.filter(deleted=True))
        return_list = set(person + department)
        return_list = serializers.serialize('json', return_list)
        return HttpResponse(return_list, content_type='application/json')


@csrf_exempt
def on_interview(request):
    if not login_required(request):
        return HttpResponse('Authenticate error')
    if request.method == 'POST':
        try:
            student_id = request.POST['stu_id']
            interviewer_name = request.POST['inter']
            profession_rate = int(request.POST['profession'])
            cooperation_rate = int(request.POST['cooper'])
            general_rate = int(request.POST['general'])
        except MultiValueDictKeyError:
            return HttpResponse('Error 110')
        except ValueError:
            return HttpResponse('Error value')
        try:
            person = PersonInfo.objects.get(student_id=student_id)
        except ObjectDoesNotExist:
            return HttpResponse('Error 233')
        person.assessment_set.create(
            interviewer_name=interviewer_name,
            profession_rate=profession_rate,
            cooperation_rate=cooperation_rate,
            general_rate=general_rate
        )
        return HttpResponse('OK')
    if request.method == 'GET':
        try:
            student_id = request.GET['student_id']
            student = PersonInfo.objects.get(student_id=student_id)
        except MultiValueDictKeyError:
            return HttpResponse('Error 110')
        except ObjectDoesNotExist:
            return HttpResponse('Error 233')
        total_assessment = student.assessment_set.all()
        json_response = serializers.serialize('json', total_assessment)
        return HttpResponse(json_response, content_type='application/json')
