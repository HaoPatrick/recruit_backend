from django.http import HttpResponse
from api.models import AuthCookie
from django.views.decorators.csrf import csrf_exempt
from api.authenticate import user_and_password_auth
from api.authenticate import generate_token
from api.authenticate import login_required
import api.authenticate as auth
from api.query import *
from api.statistic import *
import api.utilities as utility
import json


# Create your views here.
def test(request):
    return HttpResponse('Test Failed, 233')


@csrf_exempt
def authentication(request):
    if request.method == 'POST':
        try:
            user_name = request.POST['user_name']
            pass_word = request.POST['pass_word']
            try:
                user_and_password_auth(user=user_name, password=pass_word)
            except auth.TokenError as e:
                return HttpResponse(
                    utility.message(e.value), content_type='application/json')
            response_cookie = generate_token()
            AuthCookie.objects.create(cookie_value=response_cookie)
            json_response = utility.message(response_cookie)
            return HttpResponse(json_response, content_type='application/json')
        except MultiValueDictKeyError:
            return HttpResponse(
                utility.message('Authenticate failed'), content_type='application/json')
        except Exception as e:
            return HttpResponse(
                utility.message(e), content_type='application/json')
    else:
        return HttpResponse(
            utility.message('Authenticate failed'), content_type='application/json')


@csrf_exempt
def save_person_info(request):
    if request.method == 'POST':
        response_message = save_a_person_to_database(request)
    else:
        response_message = 'Error 233'
    response_message = {
        "message": response_message
    }
    return HttpResponse(json.dumps(response_message))


def get_detailed_person(request):
    """If exclude in the GET body,
        print
        """
    if not login_required(request):
        return HttpResponse('Authenticate failed')
    if request.method == 'GET':
        if request.GET.get('exclude'):
            json_person = detail_person_exclude_query(request)
        elif request.GET.get('print'):
            json_person = print_specific_department(request)
        else:
            json_person = detail_person_combine_query(request)
        return HttpResponse(json_person, content_type='application/json')
    else:
        return HttpResponse(utility.message('Error 110'))


def retrieve_person(request):
    """
    Performance issues.
    Return Persons grouped by pages
    :param request:
    :return:
    """
    if not login_required(request):
        return HttpResponse('Authenticate Failed')
    if request.method == 'GET':
        query_start = 0
        query_end = 0
        all_person = PersonInfo.objects.all().exclude(deleted=True)
        if request.GET.get('page'):
            page_number = request.GET['page']
            try:
                page_number = int(page_number) - 1
            except ValueError:
                return HttpResponse(utility.message('Error 110'))
            json_response = all_person[page_number * 20:page_number * 20 + 20]
        else:
            try:
                if request.GET.get('start'):
                    query_start = int(request.GET['start'])
                if request.GET.get('end'):
                    query_end = int(request.GET['end'])
            except ValueError:
                return HttpResponse(utility.message('Error 110'))
            if query_end > query_start >= 0:
                json_response = all_person[query_start:query_end]
            elif query_start != 0 and query_end == 0:
                json_response = all_person[query_start:]
            elif query_end == 0 and query_start == 0:
                json_response = all_person
            else:
                return HttpResponse(utility.message('Error 110'))
        json_response = list(map(utility.deserialize_person, json_response))
        json_person = json.dumps(json_response)
        return HttpResponse(json_person, content_type='application/json')


@csrf_exempt
def manage_each_person(request):
    if not login_required(request):
        return HttpResponse('Authenticate Failed')
    if request.method == 'POST':
        inclination_one_time = ''
        inclination_two_time = ''
        if_star = 0
        try:
            student_id = request.POST['student_id']
            if request.POST.get('inc_one'):
                inclination_one_time = request.POST['inc_one']
            if request.POST.get('inc_two'):
                inclination_two_time = request.POST['inc_two']
            if request.POST.get('star'):
                if_star = int(request.POST['star'])
            person = PersonInfo.objects.filter(student_id=student_id)
        except MultiValueDictKeyError:
            return HttpResponse(utility.message('Error 110'))
        except IndexError:
            return HttpResponse(utility.message('Error 233'))
        if if_star == 1:
            for each_person in person:
                each_person.star_amount += 1
        elif if_star == 2:
            for each_person in person:
                each_person.star_amount -= 1
        if inclination_one_time:
            for each_person in person:
                each_person.inc_one_time = inclination_one_time
        if inclination_two_time:
            for each_person in person:
                each_person.inc_two_time = inclination_two_time
        for each_person in person:
            each_person.save()
        return HttpResponse(utility.message('OK'))

    return HttpResponse('Oh my bad guy')


@csrf_exempt
def department_info(request):
    if request.method == 'POST':
        if not login_required(request):
            return HttpResponse('Authenticate Failed')
        try:
            nick_name = request.POST['niname']
            name = request.POST['name']
            desc = request.POST['desc']
            question = request.POST['ques']
        except MultiValueDictKeyError:
            return HttpResponse(utility.message('Error 110'))
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
        return HttpResponse(utility.message('OK'))
    elif request.method == 'GET':
        if request.GET.get('stats'):
            json_response = get_stats_via_department()
        else:
            json_response = get_department_info(request)

        if json_response:
            return HttpResponse(json_response, content_type='application/json')
        else:
            return HttpResponse(utility.message('Error 110'))


@csrf_exempt
def delete_item(request):
    if not login_required(request):
        return HttpResponse('Authenticate Failed')
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
                student = PersonInfo.objects.filter(student_id=student_id)
            except ObjectDoesNotExist:
                return HttpResponse('Does not exist')
            if recover_signal == '1':
                for stu in student:
                    stu.deleted = False
                    stu.save()
            else:
                for stu in student:
                    stu.deleted = True
                    stu.save()
        if request.POST.get('assessment'):
            try:
                recover_signal = request.POST['recover']
                if request.POST.get('stu_id'):
                    student = PersonInfo.objects.get(
                        student_id=request.POST['stu_id'])
                elif request.POST.get('stu_pk'):
                    student = PersonInfo.objects.get(pk=request.POST['stu_pk'])
                else:
                    raise MultiValueDictKeyError
                assess_pk = int(request.POST['pk'])
                assessment = student.assessment_set.get(pk=assess_pk)
            except ObjectDoesNotExist:
                return HttpResponse('Does not exist')
            except MultiValueDictKeyError:
                return HttpResponse(utility.message('Error 110'))
            if recover_signal == '1':
                assessment.deleted = False
            else:
                assessment.deleted = True
            assessment.save()
            recalculate_average_marks(student)
        return HttpResponse(utility.message('OK'))


def recycle(request):
    if request.method == 'GET':
        person = PersonInfo.objects.filter(deleted=True)
        department = Department.objects.filter(deleted=True)
        person_info_list = list(map(utility.deserialize_person, person))
        department_info_list = list(map(utility.deserialize_department, department))
        return_list = {
            "person": person_info_list,
            "department": department_info_list
        }
        return_list = json.dumps(return_list)
        return HttpResponse(return_list, content_type='application/json')


def get_stat(request):
    response = get_general_stat()
    json_response = json.dumps(response)
    return HttpResponse(json_response, content_type='application/json')
