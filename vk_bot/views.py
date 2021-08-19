import json

from django.http import HttpResponse
from django.views import View

from .handlers.message import VKMessageHandler
from mybot.settings import VK_SECRET_KEY


class VKBotWebhookView(View):
    @staticmethod
    def post(request):
        data = json.loads(request.body)
        if data.get('secret') == VK_SECRET_KEY:
            response = VKMessageHandler().handle(data)
            return response

        return HttpResponse(
            'wrong secret key',
            content_type="text/plain",
            status=403
        )

    @staticmethod
    def get(request):
        return HttpResponse('ok', content_type="text/plain", status=200)
