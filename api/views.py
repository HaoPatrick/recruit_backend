from django.http import HttpResponse
from api.models import Assessment, AuthCookie
from django.views.decorators.csrf import csrf_exempt
from api.authenticate import user_and_password_auth
from api.authenticate import generate_cookie
from api.authenticate import login_required
from api.query import *
from api.statistic import *
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
        result = save_a_person_to_database(request)
        if result:
            return HttpResponse('OK')
        else:
            return HttpResponse('Error 110')
    else:
        return HttpResponse('Error 233')


def get_detailed_person(request):
    if not login_required(request):
        return HttpResponse('Authenticate error')
    if request.method == 'GET':
        if request.GET.get('exclude'):
            json_person = detail_person_exclude_query(request)
        elif request.GET.get('print'):
            json_person = print_specific_department(request)
        else:
            json_person = detail_person_combine_query(request)
        return HttpResponse(json_person, content_type='application/json')
    else:
        return HttpResponse('Error 233')


def retrieve_person(request):
    if not login_required(request):
        return HttpResponse('Authenticate error')
    if request.method == 'GET':
        query_start = 0
        query_end = 0
        all_person = PersonInfo.objects.all().exclude(deleted=True)
        list_response = []
        dict_response = []
        for index, person in enumerate(all_person):
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
        if request.GET.get('page'):
            page_number = request.GET['page']
            try:
                page_number = int(page_number) - 1
            except ValueError:
                return HttpResponse('Erroooooooooor 110')
            json_response = list_response[page_number * 20:page_number + 20]
        else:
            try:
                if request.GET.get('start'):
                    query_start = int(request.GET['start'])
                if request.GET.get('end'):
                    query_end = int(request.GET['end'])
            except ValueError:
                return HttpResponse('Erroooooooooor 110')
            if query_end > query_start >= 0:
                json_response = list_response[query_start:query_end]
            elif query_start != 0 and query_end == 0:
                json_response = list_response[query_start:]
            elif query_end == 0 and query_start == 0:
                json_response = list_response
            else:
                return HttpResponse('Erroooooooooor 110')
        json_response.append({'total': len(list_response)})
        json_person = json.dumps(json_response)
        # json_person = serializers.serialize('json', list_response)
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
            person = PersonInfo.objects.filter(student_id=student_id)
        except MultiValueDictKeyError:
            return HttpResponse('Errrrrrrrrrrrrrrrrrror 110')
        except IndexError:
            return HttpResponse('Error 233')
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
                each_person.inc_one_time = inclination_one_time
        for each_person in person:
            each_person.save()
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
        if request.GET.get('stats'):
            json_response = get_stats_via_department()
        else:
            json_response = get_department_info(request)

        if json_response:
            return HttpResponse(json_response, content_type='application/json')
        else:
            return HttpResponse('Error 110')


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
                return HttpResponse('Error 110')
            if recover_signal == '1':
                assessment.deleted = False
            else:
                assessment.deleted = True
            assessment.save()
            recalculate_average_marks(student)
        return HttpResponse('OK')


def recycle(request):
    if request.method == 'GET':
        person = list(PersonInfo.objects.filter(deleted=True))
        department = list(Department.objects.filter(deleted=True))
        assessment = list(Assessment.objects.filter(deleted=True))
        return_list = set(person + department + assessment)
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
            comment = request.POST['comment']
            profession_rate = int(request.POST['profession'])
            cooperation_rate = int(request.POST['cooper'])
            general_rate = int(request.POST['general'])
            department_name = request.POST['depart']
            expression_ability = int(request.POST['express'])
            interesting = int(request.POST['interesting'])
        except MultiValueDictKeyError:
            return HttpResponse('Error 110')
        except ValueError:
            return HttpResponse('Error value')
        try:
            department = Department.objects.get(name=department_name)
            person = department.personinfo_set.filter(student_id=student_id)[0]
        except ObjectDoesNotExist:
            return HttpResponse('Error 233')
        except IndexError:
            return HttpResponse('当前部门也许不对噢')
        person.assessment_set.create(
            interviewer_name=interviewer_name,
            profession_rate=profession_rate,
            cooperation_rate=cooperation_rate,
            general_rate=general_rate,
            comment=comment,
            expression_ability=expression_ability,
            interesting=interesting
        )
        department.assess_count += 1
        department.save()
        # TODO: Performance improvement
        total_assessment_count = Assessment.objects.filter(deleted=False).count()
        if not total_assessment_count % 30:
            all_assessment = Assessment.objects.all().filter(deleted=False)
            all_pro = [ass.profession_rate for ass in all_assessment]
            all_cooper = [ass.cooperation_rate for ass in all_assessment]
            all_general = [ass.general_rate for ass in all_assessment]
            all_express = [ass.expression_ability for ass in all_assessment]
            all_interesting = [ass.interesting for ass in all_assessment]

            average_pro = sum(all_pro) / float(len(all_pro))
            average_cooper = sum(all_cooper) / float(len(all_cooper))
            average_general = sum(all_general) / float(len(all_general))
            average_express = sum(all_express) / float(len(all_express))
            average_interesting = sum(all_interesting) / float(len(all_interesting))

            all_department = Department.objects.all().filter(deleted=False)
            all_department.update(average_pro=average_pro,
                                  average_cooper=average_cooper,
                                  average_interesting=average_interesting,
                                  average_general=average_general,
                                  average_expression=average_express)
        # Update average assessment rate of the person
        recalculate_average_marks(person)
        return HttpResponse('OK')
    if request.method == 'GET':
        if request.GET.get('student_id'):
            try:
                student_id = request.GET['student_id']
                student = PersonInfo.objects.filter(student_id=student_id)[0]
            except MultiValueDictKeyError:
                return HttpResponse('Error 110')
            except ObjectDoesNotExist:
                return HttpResponse('Error 233')
            total_assessment = student.assessment_set.all().filter(deleted=False)
            json_response = serializers.serialize('json', total_assessment)
        elif request.GET.get('rank'):
            json_response = get_ranked_person_via_department(request)
        else:
            json_response = False

        if json_response:
            return HttpResponse(json_response, content_type='application/json')
        else:
            return HttpResponse('Error 110')


def get_stat(request):
    response = get_general_stat()
    json_response = json.dumps(response)
    return HttpResponse(json_response, content_type='application/json')
