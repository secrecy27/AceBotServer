from django.conf.urls import url, include
from rest_framework import routers

from api import views

"""
View 클래스 대신 ViewSet 클래스를 사용했기때문에
URL 설정할 필요가 없음.
Router를 사용하면 뷰코드와 뷰, URL이 자동 연결된다.
나머지는 REST 프레임워크가 알아서 다 한다.
"""

router = routers.DefaultRouter()
router.register(r'messages', views.MessageViewSet)

urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^api-v1/', include('rest_framework.urls', namespace='rest_framework_category'))
]