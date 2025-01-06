import json
import google.generativeai as genai
from django.conf import settings
from django.core import serializers
from outflows.models import Outflow
from products.models import Product
from ai import prompts, models


class SGEAgent:
    def __init__(self):
        genai.configure(api_key=settings.GEMINI_API_KEY)
        self.__client = genai.GenerativeModel(settings.GEMINI_MODEL)

    def __get_data(self):
        outflows = Outflow.objects.all()
        products = Product.objects.all()
        return json.dumps({
            'outflows': serializers.serialize('json', outflows),
            'products': serializers.serialize('json', products),
        })

    def invoke(self):
        chat = self.__client.start_chat(
            history=[
                {"role": "model", "parts": prompts.MODEL_PROMPT}
            ]
        )
        response = chat.send_message(
            prompts.USER_PROMPT.replace("{{data}}", self.__get_data()),
            generation_config=genai.types.GenerationConfig(
                max_output_tokens=1000
            )
        )
        models.AIResult.objects.create(result=response.text)
