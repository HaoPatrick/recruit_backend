def check_if_spam(form_data):
    if len(str(form_data['question_one']) +
                   str(form_data['question_two']) +
                   str(form_data['question_tree'])) < 50:
        return True
    return False
