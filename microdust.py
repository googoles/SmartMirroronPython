import json
import requests

your_province = '' # Type your Province
gov_api_key = '' # Type your API key
microdust_req_url = 'http://openapi.airkorea.or.kr/openapi/services/rest/ArpltnInforInqireSvc/getCtprvnMesureSidoLIst?serviceKey=%s&numOfRows=10&pageNo=1&sidoName=%s&searchCondition=DAILY&_returnType=json' % (gov_api_key, your_province)
dustdata = requests.get(microdust_req_url).text
dust_data = json.loads(dustdata)
my_city = dust_data['list'][1]
pm10 = my_city['pm10Value']
pm25 = my_city['pm25Value']
print(pm10)
print(pm25)