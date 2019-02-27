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

        # className에 카테고리 추가, conversation 디렉터리안의 파일로 참조
        className = ["daios", "member", "private_sale", "homepage", "greeting", "morning",
                     "lunch", "congratulations", "laugh", "ella",
                     "whitepaper", "event", "advertising", "weather", "dirtcast"]
        condition = {"whitepaper": {"word": "백서"}, "event": {"word": "이벤트"},
                     "advertising": {"length": "100", "word": "http"}}

        if high_class in className:
            if high_class in condition:
                for k in condition[high_class].keys():
                    # k = word, length
                    if k in "length":
                        if len(question) > int(condition[high_class][k]):
                            return self.process_answer(high_class)
                        else:
                            return "noData"
                    else:
                        if condition[high_class][k] in question:
                            return self.process_answer(high_class)
                        else:
                            return "noData"
                        # print("11",condition[high_class][k])
                        # if str(i for i in condition[high_class][k]) in question:
                        #     print("있음")
                        # else:
                        #     print("here : ",(i for i in condition[high_class][k]))
                        #     print("없음")
            else:
                return self.process_answer(high_class)
        else:
            return "noData"

    @staticmethod
    def process_answer(answer_class):
        base_path = "answer/"
        condition = ["weather","dirtcast"]

        if answer_class in condition : # 단일 파일 내용을 통째로 반환
            with open(base_path + answer_class, "r", encoding="utf-8") as f:
                lines = f.readlines()
                answer = ''
                for line in lines:
                    answer = answer + str(line)
                return answer

        else : # 파일 내용을 라인별 무작위 반환
            with open(base_path + answer_class, "r", encoding="utf-8") as f:
                lines = f.readlines()
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
        if serializer.is_valid():
            self.perform_create(serializer)

        return JsonResponse(result)
