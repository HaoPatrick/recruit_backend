from api.models import PersonInfo


def get_general_stat():
    all_correct_person = PersonInfo.objects.filter(deleted=False)
    response_list = []
    gender_dict = {}
    date_day_dict = {}
    date_month_dict = {}
    date_hour_dict = {}
    date_weekday_dict = {}
    device_detail_list = [{'name': 'Android', 'value': 0},
                          {'name': 'iOS', 'value': 0},
                          {'name': 'Windows', 'value': 0}]
    device_browser_list = [
        {'name': 'WeChat', 'value': 0},
        {'name': 'Chrome', 'value': 0},
        {'name': 'IE', 'value': 0},
        {'name': 'Edge', 'value': 0},
        {'name': 'Firefox', 'value': 0}
    ]
    for person in all_correct_person:
        if str(person.date_time.day) in date_day_dict:
            date_day_dict[str(person.date_time.day)] += 1
        else:
            date_day_dict[str(person.date_time.day)] = 1

        if str(person.date_time.month) in date_month_dict:
            date_month_dict[str(person.date_time.month)] += 1
        else:
            date_month_dict[str(person.date_time.month)] = 1

        if str(person.date_time.hour) in date_hour_dict:
            date_hour_dict[str(person.date_time.hour)] += 1
        else:
            date_hour_dict[str(person.date_time.hour)] = 1

        if str(person.date_time.weekday()) in date_weekday_dict:
            date_weekday_dict[str(person.date_time.weekday())] += 1
        else:
            date_weekday_dict[str(person.date_time.weekday())] = 1

        if person.gender in gender_dict:
            gender_dict[person.gender] += 1
        else:
            gender_dict[person.gender] = 1

        user_agent = person.user_agent
        if 'Windows' in user_agent:
            device_detail_list[2]['value'] += 1
        elif 'Android' in user_agent:
            device_detail_list[0]['value'] += 1
        elif 'iPhone' in user_agent:
            device_detail_list[1]['value'] += 1

        if 'MicroMessenger' in user_agent:
            device_browser_list[0]['value'] += 1
        elif 'Edge' in user_agent:
            device_browser_list[3]['value'] += 1
        elif 'IE' in user_agent:
            device_browser_list[2]['value'] += 1
        elif 'Firefox' in user_agent:
            device_browser_list[4]['value'] += 1
        elif 'Chrome' in user_agent:
            device_browser_list[1]['value'] += 1

    gender_list = []
    date_hour_list = []
    date_weekday_list = []
    date_day_list = []
    date_month_list = []
    for key, value in gender_dict.items():
        gender_list.append({'value': value, 'name': key})
    for key, value in date_hour_dict.items():
        date_hour_list.append({'value': value, 'name': key})
    for key, value in date_weekday_dict.items():
        date_weekday_list.append({'value': value, 'name': key})
    for key, value in date_day_dict.items():
        date_day_list.append({'value': value, 'name': key})
    for key, value in date_month_dict.items():
        date_month_list.append({'value': value, 'name': key})
    response_list.append({'gender': gender_list,
                          'date': {
                              'hour': date_hour_list,
                              'month': date_month_list,
                              'weekday': date_weekday_list,
                              'day': date_day_list},
                          'device': {
                              'general': device_detail_list,
                              'browser': device_browser_list
                          }
                          })
    return response_list
