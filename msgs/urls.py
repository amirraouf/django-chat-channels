from django.conf.urls import url
from msgs.views import log_in, log_out, user_list


urlpatterns = [
    url(r'^login/$', log_in, name='log_in'),
    url(r'^logout/$', log_out, name='log_out'),
    url(r'^$', user_list, name='user_list')
]
