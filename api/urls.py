from django.conf.urls import url
import api.views

urlpatterns = [
    url(r'^test$', api.views.test, name='test'),
    url(r'^save', api.views.save_person_info, name='save'),
    url(r'^person', api.views.retrieve_person, name='person'),
    url(r'^detail', api.views.get_detailed_person, name='detail'),
    url(r'^manage', api.views.manage_each_person, name='manage'),
    url(r'^auth', api.views.authentication, name='auth'),
    url(r'^department', api.views.department_info, name='department'),
    url(r'^delete', api.views.delete_item, name='delete'),
    url(r'^recycle', api.views.recycle, name='recycle'),
    # url(r'^interview', api.views.on_interview, name='interview'),
    url(r'^statistic', api.views.get_stat, name='statistic')
]
