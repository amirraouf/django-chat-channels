from django.conf.urls import url
from msgs.views import chat

urlpatterns = [
    url(r'^(?P<user>[\w.@+-]+)/$', chat, name='chat'),
]
