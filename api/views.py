from django.shortcuts import render
from django.http import HttpResponse
from api.models import PersonInfo
from django.core import serializers
from django.views.decorators.csrf import csrf_exempt, csrf_protect


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
        except Exception as e:
            return HttpResponse('errrrrrrrrrrrror')
        # TODO: Validate the post data
        new_person = PersonInfo.objects.create(
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
            photo=photo
        )
        return HttpResponse('OK')
    else:
        return HttpResponse('error')


def retrieve_person(request):
    all_person = PersonInfo.objects.all()
    json_person = serializers.serialize('json', all_person)
    return HttpResponse(json_person, content_type='application/json')
