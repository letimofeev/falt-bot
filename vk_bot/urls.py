from django.conf.urls import url
from django.views.decorators.csrf import csrf_exempt

from . import views

app_name = 'vk_bot'

urlpatterns = [
    url('', csrf_exempt(views.VKBotWebhookView.as_view()), name='index'),
]
