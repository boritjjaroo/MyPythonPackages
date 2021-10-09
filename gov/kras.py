# 국토교통부 공시가격 검색 API
import json
import requests
import datetime
from bs4 import BeautifulSoup


# 주택공시가격열람
# 원본
# Request URL: http://kras.gyeongnam.go.kr/land_info/info/houseprice/houseprice.do;jsessionid=ytzLc1T1Qd47OfVYNlWAEcUO2uah68Psya8jCLvGrgNB6PJcpB5AXaU31aLhBrb5?service=housePriceInfo
# Request Method: POST

kras_house_price_url_scheme = 'http:'
kras_house_price_url_hosts = {
    '48' : 'kras.gyeongnam.go.kr',
    '47' : 'kras.gb.go.kr'
}
kras_house_price_url_path = '/land_info/info/houseprice/houseprice.do'
kras_house_price_url_query = ';jsessionid=ytzLc1T1Qd47OfVYNlWAEcUO2uah68Psya8jCLvGrgNB6PJcpB5AXaU31aLhBrb5?service=housePriceInfo'

# Request Header

header = {
    #Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9
    #Accept-Encoding: gzip, deflate
    #Accept-Language: ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7
    #Cache-Control: max-age=0
    #Connection: keep-alive
    'Content-Length': '201',
    'Content-Type': 'application/x-www-form-urlencoded',
    #Cookie: JSESSIONID=ytzLc1T1Qd47OfVYNlWAEcUO2uah68Psya8jCLvGrgNB6PJcpB5AXaU31aLhBrb5
    'Host': 'kras.gyeongnam.go.kr',
    'Origin': 'kras.gyeongnam.go.kr',
    'Referer': 'http://kras.gyeongnam.go.kr/land_info/info/houseprice/houseprice.do',
    #Upgrade-Insecure_Requests: 1
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.61 Safari/537.36',
}

class HousePriceInfo:
    def __init__(self):
        date = None
        number = 0
        address_road = ''
        area_t = 0.0
        area_e = 0.0
        total_area_t = 0.0
        total_area_e = 0.0
        price = 0

    def __repr__(self):
        str = f'{self.address_road} {self.area_t} {self.total_area_t} {self.date} {self.price}'
        return str

def get_house_price(lawd_cd, bonbun, bubun):
    result = []

    url_host = kras_house_price_url_hosts[lawd_cd[0:2]]
    url_path = kras_house_price_url_scheme + '//' + url_host + kras_house_price_url_path
    url = url_path + kras_house_price_url_query

    header['Host'] = url_host
    header['Origin'] = url_host
    header['Referer'] = url_path

    data = {}
    data['service'] = ''
    landcode = f'{lawd_cd}1{bonbun:0>4}{bubun:0>4}'
    data['landcode'] = landcode
    data['fromYear'] = '2005'
    data['toYear'] = '2021'
    data['dongNo'] = ''
    data['addrNm'] = ''
    data['bobn'] = bonbun
    data['bubn'] = bubun
    # 1: 일반, 2: 산, ...
    data['selectLandType'] = '1'
    data['bonbun'] = '0000'
    data['bubun'] = '0000'
    data['roadCd'] = ''
    data['umdSeq'] = ''
    data['roadNm'] = ''
    data['dongCnt'] = '01'
    data['trans_land_cd'] = ''
    data['trans_sgg_cd'] = ''

    response = requests.post(url, headers=header, data=data)

    if response.status_code != 200 :
        print(f'Http error : {response.status_code}')
        return result

    #response 데이터 확인
    #print(response.content)

    encoding = response.headers['Content-Type'].split(';')[1].split('=')[1]
    soup = BeautifulSoup(response.content, 'html5lib', from_encoding=encoding)
    tag_table = soup.find('table', class_='table0202 mt-10')
    if not tag_table:
        return result

    trs = tag_table.tbody.find_all('tr')
    if not trs or len(trs) < 4:
        return result

    tds = trs[3].find_all('td')
    if not tds or len(tds) < 8:
        return result

    info = HousePriceInfo()
    ymd = tds[0].text.strip().split('/')
    info.date = datetime.date(int(ymd[0]), int(ymd[1]), int(ymd[2]))
    info.number = int(tds[1].text.strip())
    info.address_road = tds[2].text.strip()
    info.area_t = float(tds[3].text.strip())
    info.area_e = float(tds[4].text.strip())
    info.total_area_t = float(tds[5].text.strip())
    info.total_area_e = float(tds[6].text.strip())
    info.price = int(tds[7].text.strip().replace(',',''))
    result.append(info)

    return result


if __name__ == "__main__":
    #print(get_house_price('4785025324', '14', '14'))
    print(get_house_price('4719025332', '1138', ''))
    print(get_house_price('4833011400', '185', '5'))
