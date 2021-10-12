import requests
import json

class Nsdi:
    def __init__(self):
        pass
    def __repr__(self):
        str = f''
        return str

    @staticmethod
    def json_get(json_object, key, default):
        val = json_object.get(key)
        if not val:
            val = default
        return val

    @staticmethod
    def pnu(lawd_cd, is_san, bonbun, bubun):
        if is_san:
            is_san_cd = 2
        else:
            is_san_cd = 1
        result = f'{lawd_cd}{is_san_cd}'
        if isinstance(bonbun, str) and bonbun:
            bonbun_s = f'{bonbun:0>04}'
            bonbun_s = bonbun_s.replace('*', '')
            result += bonbun_s
        elif isinstance(bonbun, int):
            result += f'{bonbun:04}'
        if isinstance(bubun, str) and bubun:
            bubun_s = f'{bubun:0>04}'
            bubun_s = bubun_s.replace('*', '')
            result += bubun_s
        elif isinstance(bubun, int):
            result += f'{bubun:04}'
        return result

    @staticmethod
    def search(url, lawd_cd, is_san, bonbun, bubun, year=None, rows=None, page=None):
        return Nsdi.search_(url, Nsdi.pnu(lawd_cd, is_san, bonbun, bubun), year, rows, page)

    @staticmethod
    def search_(url, pnu, year=None, rows=None, page=None):
        result = []

        headers = {
            #Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9
            #Accept-Encoding: gzip, deflate
            #Accept-Language: ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7
            #Cache-Control: max-age=0
            #Connection: keep-alive
            'Cookie': 'JSESSIONID=0ACD417D9E66BDF16AF48EF68CF495BA; _TRK_CR=http%3A%2F%2Fwww.nsdi.go.kr%2F; _TRK_UID=29187586ae00bcc6f61f26617f40f268:2; _TRK_SID=fe000f88c42ea4548f03a7a8d3a8f0e1; _TRK_CQ=%3FsvcSe=S%26svcId=S027; _TRK_EX=17',
            'Host': 'openapi.nsdi.go.kr',
            'Referer': 'http://openapi.nsdi.go.kr/nsdi/eios/OperationSumryDetail.do',
            #Upgrade-Insecure-Requests: 1
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.71 Safari/537.36',
        }
        params = {
            # cookie를 이용해 인증키 우회
            #'authkey': '',
            'format': 'json',
            'numOfRows': '1000',
            'pageNo': '1',
        }
            # pnu : 법정동코드(10) + 일반/산(1) + 본번(4) + 부번(4)
        params['pnu'] = pnu
        if year:
            params['stdrYear'] = f'{year}'
        if rows:
            params['numOfRows'] = f'{rows}'
        if page:
            params['pageNo'] = f'{page}'

        response = requests.get(url, params=params, headers=headers)
        if response.status_code != 200 :
            print(url)
            print(f'Http error : {response.status_code}')
            return result

        #response 데이터 확인
        #print(response.content)

        json_data = json.loads(response.content)
        return json_data

        
if __name__ == "__main__":
    print(Nsdi.pnu('4833025324', 0, 508, 14))
    print(Nsdi.pnu('4833025324', 0, '508', ''))
    print(Nsdi.pnu('4833025324', 0, '5**', ''))
    print(Nsdi.pnu('4833025324', 0, '508', '1*'))
