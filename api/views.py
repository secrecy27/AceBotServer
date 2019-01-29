import os
from random import randint

from django.http import JsonResponse
from rest_framework import viewsets
from rest_framework.decorators import action, api_view

from api.classification import Naive_bayes
from .models import Message
from .serializers import MessageSerializer


class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer

    def process_request(self, question):
        n = Naive_bayes()
        high_class, high_score = n.classify(question)
        print("question : ", question, "/ class : ", high_class, "/ score : ", high_score)

        if (high_class == "daios"):
            return self.process_answer(high_class)
        elif (high_class == "whitepaper" and "백서" in question):
            return self.process_answer(high_class)
        elif (high_class == "member"):
            return self.process_answer(high_class)
        elif (high_class == "private_sale"):
            return self.process_answer(high_class)
        elif (high_class == "homepage"):
            return self.process_answer(high_class)
        else:
            return "noData"

    @staticmethod
    def process_answer(answer_class):
        base_path = "answer/"
        with open(base_path + answer_class, "r", encoding="utf-8") as f:
            lines=f.readlines()
            number = len(lines)
            i = randint(1, number)
            answer = lines[i - 1]
            return answer

    def create(self, request, *args, **kwargs):
        person = request.data['person']
        text = request.data['text']
        answer = self.process_request(text)

        result = {}
        result['person'] = person
        result['text'] = text
        result['subText'] = "단체방"
        result['answer'] = answer

        serializer = self.get_serializer(data=request.data)
        if (serializer.is_valid()):
            self.perform_create(serializer)
        return JsonResponse(result, status=201)
