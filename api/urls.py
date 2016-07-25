from django.conf.urls import patterns, url
import api.views

urlpatterns = [
    url(r'^test$', api.views.test, name='test'),
    url(r'^save', api.views.save_person_info, name='save'),
    url(r'^retrieve', api.views.retrieve_person, name='retrieve'),
]
