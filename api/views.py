from random import randint
from django.http import JsonResponse
from rest_framework import viewsets
from rest_framework.decorators import action, api_view

from api.classification import Naive_bayes
from .models import Message
from .serializers import MessageSerializer
import os


class MessageViewSet (viewsets.ModelViewSet):
    def check_call_bot(self, question):
        bot_name = '엘라'
        if bot_name in question:
            return True
        else:
            return False

    def remove_bot_name(self, question):

        question = question.replace('엘라야','')
        question = question.replace('엘라', '')
        return question

    queryset = Message.objects.all()
    serializer_class = MessageSerializer

    def process_request(self, question):
        if self.check_call_bot(question) == True:
            question_no_botname = self.remove_bot_name(question)  # 비교시 엘라 단어 제거
            n = Naive_bayes()
            high_class, high_score = n.classify(question_no_botname)

            call_bot_name = ["엘라야", "엘라님", "엘라", "엘라씨"]
            if question in call_bot_name:
                high_class = "ella"
                high_score = 1

            print("question : ", question, "/ class : ", high_class, "/ score : ", high_score)

            path = os.path.dirname(os.path.realpath(__file__))+'/../conversation'

            
            className = []
            for fileName in os.listdir(path): # conversation 경로의 파일들을 className 리스트 삽입
                className.append(fileName)
           
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
        else :
            return "noData"

    @staticmethod
    def process_answer(answer_class):
        base_path = "answer/"
        condition = ["weather","dirtcast","predict_coin"]

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
