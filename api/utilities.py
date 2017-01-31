import json


def deserialize_person(person):
    result = {
        "model": "person",
        "pk": person.pk,
        "fields": {
            "name": person.name,
            "gender": person.gender,
            "inc_one": person.inclination_one,
            "inc_two": person.inclination_two,
            "major": person.major,
            "mail": person.mail_address,
            "is_spam": person.is_spam,
            "phone_number": person.phone_number,
            "photo": person.photo,
            "question_one": person.question_one,
            "question_two": person.question_two,
            "self_intro": person.self_intro,
            "share_work": person.share_work,
            "star": person.star_amount,
            "student_id": person.student_id,
            "time_spend": person.time_spend,
            "UA": person.user_agent,
            "deleted": person.deleted
        }
    }
    return result


def deserialize_department(department):
    result = {
        "model": "department",
        "pk": department.pk,
        "fields": {
            "deleted": department.deleted,
            "name": department.name,
            "nick_name": department.nick_name,
            "question": department.question,
            "desc": department.desc
        }
    }
    return result


def message(msg):
    result = {
        "message": msg
    }
    return json.dumps(result)
