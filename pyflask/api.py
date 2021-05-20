from urllib.request import urlopen
from urllib.parse import urlencode, unquote, quote_plus
import requests
import json
from datetime import datetime
from requests.api import get

# 프로그램 설명 
print("이 프로그램은 오늘 특정 시간을 기준으로 내일, 내일 모레의 자외선 지수를 출력하는 프로그램입니다. ")

# secret 키 들어있는 secret.json 열기 
with open ("secret.json") as f: 
    # secret 변수에 json 내용 저장 
    secret = json.loads(f.read())

# 시간대 입력 받음 
now = datetime.now()
h = input("조회할 시간을 입력하세요. (ex 06, 07, .. 13)")

# api date 포맷 맞추기 
# formatday =0

# datetime 으로 
y = now.year
m = now.month
d = now.day

# 입력 값이 일의 자리일 경우, 십의 자리에 0 추가하는 함수 (ex 5 => 05)
def Formating(num) : 
    # 일의 자리일 경우, 십의 자리에 0 추가 
    if int(num) < 10 :
        formated = "0" + str(num)

    # 그 외는 그대로 출력 
    else : 
        formated = str(num)

    # 포맷팅 된 num 출력 
    return formated

# api 형식에 맞는 date 선언 
date = str(y)+Formating(m)+Formating(d)+h

# api 호출 
url = 'http://apis.data.go.kr/1360000/LivingWthrIdxService01/getUVIdx'

# 전송할 파라미터 입력 
queryParams = '?' + urlencode(
    {   
    # quote_plus : 한글은 url 들어가면 깨지기 때문에 안 깨지도록 quote_plus 를 사용함 
    # 시크릿키 json 에서 불러오기
    quote_plus('ServiceKey'): secret["SECRET_KEY"],
    quote_plus('areaNo'):'1100000000', # 지역 : 서울 # 공백이면 전체 지점을 조회합니다. 
    quote_plus('time'): date, # 포맷팅한 date 입력
    quote_plus('dataType'):'JSON' # 형식 JSON 
    }
    )

# response 를 get 형식으로 받아서 저장 
# unquote : 한글로 보내준 url 풀어줌
get_data = requests.get(url + unquote(queryParams))

# 응답 잘 받는지 확인 (코드 200이 정상 응답)
print(get_data.status_code)

# json 형식을 딕셔너리 형태로 저장 
res = get_data.json()

# 응답(header로 응답 데이터가 있는지 없는지 판별하기 위해)을 딕셔너리 형태로 저장 
headerDict = res['response']['header']


# 데이터가 없을 경우 아래의 메세지 출력 
if headerDict['resultMsg'] == 'NO_DATA' :
    print(date)
    print("데이터가 없는 시간대에요.")

# 응답 받은 데이터가 있을 경우 아래의 코드 실행 
elif headerDict['resultMsg'] == 'NORMAL_SERVICE':
    # 출력 데이터 정리 
    sunDict = (res['response']['body']['items']['item'][0]) # json 에서 body 값 저장
    today = sunDict['today'] # 오늘의 자외선 지수 value 값 저장 
    tomorrow = sunDict['tomorrow'] # 내일의 자외선 지수 value 값 저장
    theDayAfterTomorrow = sunDict['theDayAfterTomorrow'] # 내일 모레의 자외선 지수 value 값 저장 

    # 경고문을 출력하는 함수 인수로 자외선 지수 값을 받아 지수의 수치에 따라 경고문을 출력 .  
    def Warn (day) : 
        if int(day) >= 11: 
            info = "자외선 지수: 위험. 밖으로 나가지 마세요."
        elif int(day) >= 8 : 
            info = "자외선 지수 매우 높음. 외출을 삼가하세요. "
        elif int(day) >= 6 : 
            info = "자외선 지수 높음 "
        elif int(day) >= 3 : 
            info = "자외선 지수 보통 "
        else : 
            info = "자외선 지수 낮음"

        # 경고 메세지를 리턴 
        return(info)

    # 경고문을 리턴한다. 
    print(date)
    print("발표 시각 : " + sunDict['date'])
    print("오늘 예측 값 : " + today +" " + Warn(today))
    print("내일 예측 값 : " + tomorrow + " " +Warn(tomorrow))
    print("내일 모레 예측 값 : " + theDayAfterTomorrow +" "+ Warn(theDayAfterTomorrow))
