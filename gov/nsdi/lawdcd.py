import requests
import json
from gov.nsdi.base import Nsdi

# 국가공간정보포털(openapi.nsdi.go.kr)
# 법정동조회서비스

class LawdCD:

    def __init__(self):
        self.code = ''
        self.name = ''
        self.full_name = ''
        pass

    def __repr__(self):
        str = f'[{self.code}] {self.name}'
        return str

    @staticmethod
    def search(lawd_cd=None):
        result = []

        if not lawd_cd:
            url = f'http://openapi.nsdi.go.kr/nsdi/eios/service/rest/AdmService/admCodeList.json'
        elif len(lawd_cd) == 2:
            url = f'http://openapi.nsdi.go.kr/nsdi/eios/service/rest/AdmService/admSiList.json'
        elif len(lawd_cd) == 5:
            url = f'http://openapi.nsdi.go.kr/nsdi/eios/service/rest/AdmService/admDongList.json'
        elif len(lawd_cd) == 8:
            url = f'http://openapi.nsdi.go.kr/nsdi/eios/service/rest/AdmService/admReeList.json'
        else:
            return result

        params = {
            # cookie를 이용해 인증키 우회
            #'authkey': '',
        }

        params['admCode'] = lawd_cd

        response = requests.get(url, headers=Nsdi.headers, params=params)
        if response.status_code != 200 :
            print(url)
            print(f'Http error : {response.status_code}')
            return result

        #response 데이터 확인
        #print(response.content)

        json_data = json.loads(response.content)
        root = json_data.get('admVOList')
        if not root:
            return result
        resultMsg = root.get('message')
        if resultMsg:
            print(f'admCodeList result message : {resultMsg}')

        list = root.get('admVOList')
        if not list:
            return result

        for item in list:
            land = LawdCD()
            land.code = item.get('admCode', '')
            land.name = item.get('lowestAdmCodeNm', '')
            land.full_name = item.get('admCodeNm', '')
            result.append(land)

        return result


if __name__ == "__main__":
    # 시도
    print(LawdCD.search())
    # 경상남도
    print(LawdCD.search('48'))
    # 경상남도 양산시
    print(LawdCD.search('48330'))
    # 경상남도 양산시 물금읍
    print(LawdCD.search('48330253'))
    # 경상남도 양산시 덕계동
    print(LawdCD.search('48330120'))
