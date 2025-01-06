import json
from django.conf import settings
from rest_framework.views import APIView, Response, status
from services.callmebot import CallMeBotService
from django.core.mail import send_mail
from django.template.loader import render_to_string
from .models import Webhook
from .messages import outflow_message


class WebhookOrderView(APIView):

    def post(self, request):
        data = request.data

        Webhook.objects.create(
            event_type=data.get('event_type'),
            event=json.dumps(data, ensure_ascii=False)
        )

        product = data.get("product")
        quantity = data.get("quantity")
        total_selling_price = data.get("product_selling_price") * quantity

        product_cost_price = data.get("product_cost_price")
        total_profit = total_selling_price - (product_cost_price * quantity)

        message = outflow_message.format(
            product,
            quantity,
            total_selling_price,
            total_profit
        )
        callmebot = CallMeBotService()
        callmebot.send_message(message)

        data['total_selling_price'] = total_selling_price
        data['total_profit'] = total_profit

        send_mail(
            subject='Nova Saída (SGE)',
            message='',
            from_email=f'SGE <{settings.EMAIL_HOST_USER}>',
            recipient_list=[settings.EMAIL_ADMIN_RECEIVER],
            html_message=render_to_string('outflow.html', data),
            fail_silently=False,
        )

        return Response(
            data=data,
            status=status.HTTP_200_OK
        )
