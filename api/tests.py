from django.test import TestCase, Client
import json
from api.models import PersonInfo, Department, AuthCookie, Assessment


# Create your tests here.
def initialize_department():
    Department.objects.create(name='技术研发中心')
    Department.objects.create(name='人力资源部门')


class NewPostTest(TestCase):
    def test_can_save_a_post(self):
        initialize_department()
        c = Client()
        response = c.post('/api/save', {
            'name': 'hao',
            'student_id': '3140102255',
            'gender': '2',
            'major': 'CS',
            'grade': '1',
            'phone_number': '13208020663',
            'self_intro': 'Hello World. Test driven development',
            'question_one': 'Hello World. Test driven development',
            'question_two': 'Hello World. Test driven development',
            'inclination_one': '技术研发中心',
            'inclination_two': '人力资源部门',
            'share_work': 'lkjasdf',
            'photo': 'photo',
            'user_agent': 'lkjas',
            'time_spend': '123456'
        })
        self.assertEqual(response.content, b'OK')
        self.assertEqual(PersonInfo.objects.count(), 1)
        new_item = PersonInfo.objects.first()
        self.assertEqual(new_item.name, 'hao')
        self.assertEqual(new_item.photo, 'photo')

    def test_do_not_get_deleted_person(self):
        PersonInfo.objects.create(name='abc', deleted=True)
        AuthCookie.objects.create(cookie_value='123')
        c = Client()
        response = c.get('/api/person', {
            'cookie': '123',
        })
        self.assertEqual(response.content, b'[]')

    def test_wrong_post_return_error(self):
        c = Client()
        response = c.post('/api/save', {
            'name': 'hao',
            'student_id': '3140102255',
            'gender': '2',
            'major': 'CS',
            'grade': '1',
            'phone_number': '13208020663',
            'self_intro': 'Hello World. Test driven development',
            'question_one': 'Hello World. Test driven development',
            'question_two': 'Hello World. Test driven development',
            'inclination_one': '技术研发中心',
            'inclination_two': '人力资源部门',
            'time_spend': '123456'
        })
        self.assertEqual(response.content, b'Error 110')
        self.assertEqual(PersonInfo.objects.count(), 0)

    def test_time_spend_type_error(self):
        c = Client()
        c.post('/api/save', {
            'name': 'hao',
            'student_id': '3140102255',
            'gender': '2',
            'major': 'CS',
            'grade': '1',
            'phone_number': '13208020663',
            'self_intro': 'Hello World. Test driven development',
            'question_one': 'Hello World. Test driven development',
            'question_two': 'Hello World. Test driven development',
            'inclination_one': '技术研发中心',
            'inclination_two': '人力资源部门',
            'share_work': 'lkjasdf',
            'photo': 'photo',
            'user_agent': 'lkjas',
            'time_spend': '123456a'
        })
        self.assertEqual(PersonInfo.objects.count(), 0)

    def test_new_post_can_overwrite_old_one(self):
        self.test_can_save_a_post()
        c = Client()
        response = c.post('/api/save', {
            'name': 'haoxiangpeng',
            'student_id': '3140102255',
            'gender': '2',
            'major': 'CS',
            'grade': '1',
            'phone_number': '13208020663',
            'self_intro': 'Hello World. Test driven development',
            'question_one': 'Hello World. Test driven development',
            'question_two': 'Hello World. Test driven development',
            'inclination_one': '技术研发中心',
            'inclination_two': '人力资源部门',
            'share_work': 'nihao',
            'photo': 'photo',
            'user_agent': 'lkjas',
            'time_spend': '123456'
        })
        self.assertEqual(response.content, b'OK')
        self.assertEqual(PersonInfo.objects.count(), 1)
        new_item = PersonInfo.objects.first()
        self.assertEqual(new_item.name, 'haoxiangpeng')
        self.assertEqual(new_item.share_work, 'nihao')


class AuthenticTest(TestCase):
    def test_success_auth(self):
        c = Client()
        response = c.post('/api/auth', {
            'user_name': 'qscqscdadada',
            'pass_word': 'ahaqsc'
        })
        json_content = json.loads(response.content.decode('utf-8'))[0]
        self.assertEqual(json_content['login'], 'OK')
        self.assertEqual(len(json_content['response_token']), 64)

    def test_wrong_password(self):
        c = Client()
        response = c.post('/api/auth', {
            'user_name': 'qscqscdadada',
            'pass_word': 'qsc'
        })
        self.assertEqual(response.content, b'Authenticate failed')

    def test_missing_param(self):
        c = Client()
        response = c.post('/api/auth', {
            'user_name': 'qscqscdadada'
        })
        self.assertEqual(response.content, b'Authenticate failed')


class RetrievePersonInfo(TestCase):
    def test_can_retrieve_a_person(self):
        initialize_department()
        c = Client()
        response = c.post('/api/auth', {
            'user_name': 'qscqscdadada',
            'pass_word': 'ahaqsc'
        })
        json_content = json.loads(response.content.decode('utf-8'))[0]
        token = json_content['response_token']
        c.post('/api/save', {
            'name': 'hao',
            'student_id': '3140102255',
            'gender': '2',
            'major': 'CS',
            'grade': '1',
            'phone_number': '13208020663',
            'self_intro': 'Hello World. Test driven development',
            'question_one': 'Hello World. Test driven development',
            'question_two': 'Hello World. Test driven development',
            'inclination_one': '技术研发中心',
            'inclination_two': '人力资源部门',
            'share_work': 'lkjasdf',
            'photo': 'photo',
            'user_agent': 'lkjas',
            'time_spend': '123456'
        })
        self.assertEqual(PersonInfo.objects.count(), 1)
        detail_response = c.get('/api/detail', {
            'cookie': token,
            'student_id': '3140102255'
        })
        json_detail = json.loads(detail_response.content.decode('utf-8'))[0]
        self.assertEqual(json_detail['fields']['name'], 'hao')
        self.assertEqual(json_detail['fields']['photo'], 'photo')


class DepartmentManage(TestCase):
    def test_save_info(self):
        AuthCookie.objects.create(cookie_value='123')
        c = Client()
        response = c.post('/api/department', {
            'niname': 'tech',
            'name': '技术研发中心',
            'desc': '全浙大最强技术',
            'ques': '你是咸鱼吗？',
            'cookie': '123'
        })
        self.assertEqual(response.content, b'OK')
        current_depart = Department.objects.first()
        self.assertEqual(current_depart.name, '技术研发中心')
        self.assertEqual(current_depart.desc, '全浙大最强技术')

    def test_without_token(self):
        c = Client()
        response = c.post('/api/department', {
            'name': '技术研发中心',
            'desc': '全浙大最强技术',
            'ques': '你是咸鱼吗？'
        })
        self.assertEqual(response.content, b'Authenticate error')
        self.assertEqual(Department.objects.count(), 0)

    def test_retrieve_info(self):
        Department.objects.create(name='tech', desc='abc', question='haha')
        AuthCookie.objects.create(cookie_value='123')
        c = Client()
        response = c.get('/api/department', {
            'name': 'tech',
            'cookie': '123'
        })
        json_response = json.loads(response.content.decode('utf-8'))[0]
        self.assertEqual(json_response['name'], 'tech')
        self.assertEqual(json_response['desc'], 'abc')
        self.assertEqual(json_response['question'], 'haha')

    def test_multi_entry(self):
        AuthCookie.objects.create(cookie_value='123')
        Department.objects.create(nick_name='tech', name='tech', desc='abc', question='haha')
        c = Client()
        response = c.post('/api/department', {
            'niname': 'tech',
            'name': 'tech',
            'cookie': '123',
            'desc': 'def',
            'ques': '233'
        })
        self.assertEqual(response.content, b'OK')
        target_depart = Department.objects.first()
        self.assertEqual(target_depart.desc, 'def')
        self.assertEqual(target_depart.question, '233')

    def test_fetch_all(self):
        AuthCookie.objects.create(cookie_value='123')
        Department.objects.create(nick_name='tech',
                                  name='tech',
                                  desc='asb',
                                  question='aaa')
        Department.objects.create(nick_name='bala',
                                  name='haha',
                                  desc='aslkdj',
                                  question='aaa')
        c = Client()
        response = c.get('/api/department', {
            'cookie': '123'
        })
        json_response = json.loads(response.content.decode('utf-8'))
        self.assertEqual(json_response[0]['nick_name'], 'tech')
        self.assertEqual(json_response[1]['question'], 'aaa')

    def test_delete_department(self):
        AuthCookie.objects.create(cookie_value='123')
        Department.objects.create(nick_name='tech',
                                  name='tech',
                                  desc='asb',
                                  question='aaa')
        c = Client()
        response = c.post('/api/delete', {
            'cookie': '123',
            'recover': '0',
            'nick_name': 'tech'
        })
        self.assertEqual(response.content, b'OK')
        self.assertEqual(Department.objects.first().deleted, True)


def initialize_database():
    AuthCookie.objects.create(cookie_value='123')
    PersonInfo.objects.create(name='name', student_id='123', gender='3', deleted=True)
    Department.objects.create(nick_name='123', name='abc', deleted=True)

    temp_depart = Department.objects.create(nick_name='233', name='a2c', deleted=False)
    temp_person = temp_depart.personinfo_set.create(name='name2', student_id='234', gender='2', deleted=False)
    temp_person.assessment_set.create(interviewer_name='aha', profession_rate=5, comment='123',
                                      cooperation_rate=3, general_rate=4, deleted=False)
    # temp_person.assessment_set.create(interviewer_name='aha', profession_rate=5, comment='123',
    #                                   cooperation_rate=3, general_rate=4, deleted=False)


class RecycleTest(TestCase):
    def test_can_retrieve(self):
        initialize_database()
        c = Client()
        response = c.get('/api/recycle', {
            'cookie': '123'
        })
        json_response = json.loads(response.content.decode('utf-8'))
        self.assertEqual(json_response[0]['fields']['name'], 'name')

    def test_recover_retrieve(self):
        initialize_database()
        c = Client()
        c.post('/api/delete', {
            'cookie': '123',
            'student_id': '123',
            'recover': '1'
        })
        self.assertEqual(PersonInfo.objects.first().deleted, False)

    def test_wont_get_deleted_department(self):
        initialize_database()
        c = Client()
        response = c.get('/api/department', {
            'cookie': '123'
        })
        response = json.loads(response.content.decode('utf-8'))
        self.assertEqual(len(response), 1)
        self.assertEqual(Department.objects.count(), 2)


class AssessmentTest(TestCase):
    def test_can_save_assessment(self):
        initialize_database()
        c = Client()
        response = c.post('/api/interview', {
            'cookie': '123',
            'stu_id': '234',
            'inter': 'hao',
            'profession': '10',
            'cooper': '8',
            'depart': 'a2c',
            'general': '10',
            'comment': '123',
            'express': '123',
            'interesting': '123'
        })
        self.assertEqual(response.content.decode('utf-8'), 'OK')
        new = Assessment.objects.get(interviewer_name='hao')
        self.assertEqual(new.profession_rate, 10)

    def test_can_retrieve_assessment(self):
        initialize_database()
        c = Client()
        response = c.get('/api/interview', {
            'cookie': '123',
            'student_id': '234'
        })
        response = json.loads(response.content.decode('utf-8'))
        self.assertEqual(len(response), 1)
        self.assertEqual(response[0]['fields']['interviewer_name'], 'aha')

    def test_can_delete_assessment(self):
        initialize_database()
        c = Client()
        self.assertEqual(Assessment.objects.filter(deleted=False).count(), 1)
        response = c.post('/api/delete', {
            'cookie': '123',
            'recover': '0',
            'assessment': '1',
            'stu_id': '234',
            'pk': '1'
        })
        self.assertEqual(response.content, b'OK')
        self.assertEqual(Assessment.objects.filter(deleted=True).count(), 1)

    def test_can_recover_assessment(self):
        initialize_database()
        assessment = Assessment.objects.first()
        assessment.deleted = True
        assessment.save()
        self.assertEqual(Assessment.objects.filter(deleted=False).count(), 0)
        c = Client()
        response = c.post('/api/delete', {
            'cookie': '123',
            'recover': '1',
            'assessment': '1',
            'stu_id': '234',
            'pk': '1'
        })
        self.assertEqual(response.content, b'OK')
        self.assertEqual(Assessment.objects.filter(deleted=True).count(), 0)
        self.assertEqual(Assessment.objects.filter(deleted=False).count(), 1)
