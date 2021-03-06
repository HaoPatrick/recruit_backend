from django.test import TestCase, Client
import json
from api.models import PersonInfo, Department, AuthCookie

# Create your tests here.

DELETED_PERSON = 'del_hao'
NORMAL_PERSON = 'hao'
USER_NAME = 'qscqscdadada'
PASS_WORD = 'ahaqsc'


def initialize_database():
    AuthCookie.objects.create(cookie_value='123')
    PersonInfo.objects.create(name='hao', student_id='2255', gender='3', deleted=True)
    PersonInfo.objects.create(name='test', student_id='1234', gender='3',
                              inclination_one="abc", inclination_two="bcd", user_agent='Linux Chrome Arch',
                              deleted=False)
    Department.objects.create(nick_name='123', name='abc', deleted=False)
    Department.objects.create(nick_name='234', name='bcd', deleted=False)


class YouNameItTest(TestCase):
    def test_nothing(self):
        c = Client()
        response = c.get('/api/test')
        self.assertContains(response, 'Test Failed, 233')


class NewPostTest(TestCase):
    def test_can_save_a_post(self):
        initialize_database()
        c = Client()
        response = c.post('/api/save', {
            'name': 'hao_ttt',
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
            'mail': 'hao@bao.com',
            'user_agent': 'lkjas',
            'time_spend': '123456'
        })
        self.assertEqual(response.content, b'{"message": "OK"}')
        # self.assertEqual(PersonInfo.objects.count(), 1)
        new_item = PersonInfo.objects.last()
        self.assertEqual(new_item.name, 'hao_ttt')
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
        self.assertEqual(response.content, b'{"message": "Error 110"}')
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
        pass
        #     self.test_can_save_a_post()
        #     self.assertEqual(PersonInfo.objects.count(), 1)
        #     c = Client()
        #     response = c.post('/api/save', {
        #         'name': 'haoxiangpeng',
        #         'student_id': '3140102255',
        #         'gender': '2',
        #         'major': 'CS',
        #         'grade': '1',
        #         'phone_number': '13208020663',
        #         'self_intro': 'Hello World.',
        #         'question_one': 'Hello World. Test driven development',
        #         'question_two': 'Hello World. Test driven development',
        #         'inclination_one': '技术研发中心',
        #         'inclination_two': '人力资源部门',
        #         'share_work': 'nihao',
        #         'photo': 'photo',
        #         'mail': 'hao@foo.com',
        # 'user_agent': 'lkjas',
        #         'time_spend': '123456'
        #     })
        #     self.assertEqual(response.content, b'{"message": "OK"}')
        #     self.assertEqual(PersonInfo.objects.count(), 1)
        #     new_item = PersonInfo.objects.first()
        #     self.assertEqual(new_item.name, 'haoxiangpeng')
        #     self.assertEqual(new_item.share_work, 'nihao')
        #     self.assertEqual(new_item.self_intro, 'Hello World.')

    def test_cannot_change_department(self):
        initialize_database()
        c = Client()
        response = c.post('/api/save', {
            'name': 'test',
            'student_id': '1234',
            'gender': '2',
            'major': 'CS',
            'grade': '1',
            'phone_number': '13208020663',
            'self_intro': 'Hello World. Test driven development',
            'question_one': 'Hello World. Test driven development',
            'question_two': 'Hello World. Test driven development',
            'inclination_one': 'abcd',
            'inclination_two': 'bcd',
            'share_work': 'lkjasdf',
            'photo': 'photo',
            'mail': 'hao@bao.com',
            'user_agent': 'lkjas',
            'time_spend': '123456'
        })
        json_response = json.loads(response.content.decode('utf-8'))
        self.assertEqual(json_response['message'], 'Can not change department!')

    def test_not_post(self):
        c = Client()
        response = c.get('/api/save')
        self.assertContains(response, '233')


class AuthenticTest(TestCase):
    def test_success_auth(self):
        c = Client()
        response = c.post('/api/auth', {
            'user_name': USER_NAME,
            'pass_word': PASS_WORD
        })
        json_content = json.loads(response.content.decode('utf-8'))
        self.assertNotEqual(json_content['message'], 'Authenticate failed')
        self.assertEqual(len(json_content['message']), 64)

    def test_nothing(self):
        c = Client()
        response = c.get('/api/auth')
        self.assertContains(response, 'Authenticate failed')

    def test_wrong_password(self):
        c = Client()
        response = c.post('/api/auth', {
            'user_name': USER_NAME,
            'pass_word': 'qsc'
        })
        self.assertEqual(response.content, b'{"message": "Authenticate failed"}')

    def test_missing_param(self):
        c = Client()
        response = c.post('/api/auth', {
            'user_name': USER_NAME
        })
        self.assertEqual(response.content, b'{"message": "Authenticate failed"}')


class RetrievePersonInfo(TestCase):
    def test_can_retrieve_a_person(self):
        initialize_database()
        c = Client()
        response = c.post('/api/auth', {
            'user_name': USER_NAME,
            'pass_word': PASS_WORD
        })
        json_content = json.loads(response.content.decode('utf-8'))
        token = json_content['message']
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
            'mail': 'foo@bar.com',
            'user_agent': 'lkjas',
            'time_spend': '123456'
        })
        # self.assertEqual(PersonInfo.objects.count(), 1)
        detail_response = c.get('/api/detail', {
            'cookie': token,
            'student_id': '3140102255'
        })
        json_detail = json.loads(detail_response.content.decode('utf-8'))[0]
        self.assertEqual(json_detail['fields']['name'], 'hao')
        self.assertEqual(json_detail['fields']['photo'], 'photo')

    def test_not_authenticated(self):
        c = Client()
        response = c.get('/api/detail')
        self.assertEqual(response.content.decode('utf-8'), 'Authenticate failed')

    def test_print_person_by_department(self):
        initialize_database()
        c = Client()
        response = c.get('/api/detail', {
            'print': '1',
            'cookie': '123',
            'department': 'abc'
        })
        result = json.loads(response.content.decode('utf-8'))
        self.assertEqual(result[0]['model'], 'api.personinfo')

    def test_get_exclude_query(self):
        initialize_database()
        c = Client()
        response = c.get('/api/detail', {
            'name': 'test',
            'gender': '3',
            'linux': '1',
            'cookie': '123',
            'exclude': '1'
        })
        response = json.loads(response.content.decode())
        self.assertEqual(response[0]['fields']['name'], 'test')


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
        self.assertEqual(response.content, b'{"message": "OK"}')
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
        self.assertEqual(response.content, b'Authenticate Failed')
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
        self.assertEqual(response.content, b'{"message": "OK"}')
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
        self.assertEqual(response.content, b'{"message": "OK"}')
        self.assertEqual(Department.objects.first().deleted, True)


class RecycleTest(TestCase):
    def test_can_retrieve(self):
        initialize_database()
        c = Client()
        response = c.get('/api/recycle', {
            'cookie': '123'
        })
        json_response = json.loads(response.content.decode('utf-8'))
        # print(json_response)
        self.assertEqual(json_response['person'][0]['fields']['name'], NORMAL_PERSON)

    def test_recover_retrieve(self):
        initialize_database()
        c = Client()
        c.post('/api/delete', {
            'cookie': '123',
            'student_id': '123',
            'recover': '1'
        })
        self.assertEqual(PersonInfo.objects.last().deleted, False)

    def test_wont_get_deleted_department(self):
        initialize_database()
        c = Client()
        response = c.get('/api/department', {
            'cookie': '123'
        })
        response = json.loads(response.content.decode('utf-8'))
        # self.assertEqual(len(response), 1)
        self.assertNotEqual(len(response), 0)
        # self.assertEqual(Department.objects.count(), 2)


class ManagePerson(TestCase):
    def test_can_star(self):
        initialize_database()
        c = Client()
        response = c.post('/api/manage', {
            'cookie': '123',
            'star': '1',
            'student_id': '1234'
        })
        test_person = PersonInfo.objects.get(student_id='1234')
        self.assertEqual(response.content, b'{"message": "OK"}')
        self.assertEqual(test_person.star_amount, 1)

        c.post('/api/manage', {
            'cookie': '123',
            'star': '2',
            'student_id': '1234'
        })
        test_person = PersonInfo.objects.get(student_id='1234')
        self.assertEqual(test_person.star_amount, 0)

    def test_change_time(self):
        initialize_database()
        c = Client()
        response = c.post('/api/manage', {
            'cookie': '123',
            'inc_one': 'asdf',
            'inc_two': 'lkwae',
            'student_id': '1234'
        })
        test_person = PersonInfo.objects.get(student_id='1234')
        self.assertEqual(response.content, b'{"message": "OK"}')
        self.assertEqual(test_person.inc_one_time, 'asdf')
        self.assertEqual(test_person.inc_two_time, 'lkwae')


class GetStatistic(TestCase):
    def test_can_get_stat(self):
        initialize_database()
        c = Client()
        response = c.get('/api/statistic')
        # print(json.loads(response.content.decode()))
        self.assertIsNotNone(json.loads(response.content.decode()))
