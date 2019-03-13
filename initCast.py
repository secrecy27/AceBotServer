# Add to 'crontab', Billow script will be start on per hour.
# 0 * * * * python /home/ace/ace-bot/AceBotServer/initCast.py
import urllib.request
import secrets
from bs4 import BeautifulSoup
import os


def prefixWeather():
    words = ['날씨 답변 갑니다!(방긋)\n',
             '봄이 오네요~(방긋)\n',
             '엘라는 모르는게 없죠. 날씨정보입니다.(방긋)\n'
             ]
    return secrets.choice(words)


def prefixDirt():
    words = ['미세먼지 때문에 숨이막히네요 (훌쩍)\n',
             '오늘의 미세먼지 답변 갑니다!(방긋)\n',
             '엘라도 공기청정기가 필요해요 (훌쩍)\n',
             '미세..콜록콜록!! 먼지 여기있어요. (훌쩍)\n',
             '마스크 꼭 챙기세요~ (절규)'
             ]
    return secrets.choice(words)

def sufixDirt():
    words = ['다이오스봇~ 미세먼지 지도 부탁해~'
             ]
    return secrets.choice(words)


def getWeather(): # 날씨
    url = 'http://www.weather.go.kr/weather/main.jsp'
    html = urllib.request.urlopen(url)
    bs_obj = BeautifulSoup(html, "html.parser")

    casttime = bs_obj.find("p", {"class": "info_date"})  # 예보시각
    forecast = bs_obj.find("p", {"class": "wrn-info-content"})  # 예보내용
    casttime = casttime.text
    forecast = forecast.get_text(strip=True, separator='\n')
    forecast = forecast.split('\n')
    for list in forecast : # 오늘 날씨만 출력
        if '오늘' in list :
            forecast = list
            break
    forecast = str(prefixWeather()) + str(casttime) + '\n' + str(forecast)
    print(forecast) # 출력한번 해주기
    return forecast


def getDirt(): # 미세먼지
    url = 'http://www.airkorea.or.kr/web/dustForecast?pMENU_NO=113'
    html = urllib.request.urlopen(url)
    bs_obj = BeautifulSoup(html, "html.parser")

    castDirt = bs_obj.findAll("dl", {"class": "forecast MgT50"})
    castDirt = castDirt[0]

    date = castDirt.find("dt").text # 오늘 날짜만 추출
    castDirt = castDirt.find("div", {"class": "txtbox"})
    castDirt = castDirt.text
    castDirt = date + '\n' + castDirt

    # castDirt = prefixDirt() + castDirt + '\n' + sufixDirt() # 봇 호출용
    castDirt = prefixDirt() + castDirt
    print(castDirt)
    return castDirt


def initCast(): # 파일 초기화하여 쓰기
    path = os.path.dirname(os.path.realpath(__file__))
    f = open(path + '/' + 'answer/weather', mode='w', encoding='utf-8')
    f.write(getWeather())
    f.close()
    print('write weather success.')

    f = open(path + '/' + 'answer/dirtcast', mode='w', encoding='utf-8')
    f.write(getDirt())
    f.close()
    print('write dirt success.')

# getDirt()
# getWeather()

initCast()