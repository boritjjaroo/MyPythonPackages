import requests
from urllib import parse
import xml.etree.ElementTree as ET

header = {
    #'Accept': '*/*',
    #'Accept-Encoding': 'gzip, deflate, br',
    #'Accept-Language': 'ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7',
    #'Connection': 'keep-alive',
    'Cookie': 'chrCookie1631678662738=cookieValue; idxCd_2432=2432; chrCookie1633521483671=cookieValue;JSESSIONID=7zurkSWiJRxPH4BHB17MpDFocfkIG3afpbA8SwBMz1GBn1IwpOFBpRoObyaG2yGD.wasgams2_servlet_engine1',
    'Host': 'www.index.go.kr',
    'Referer': 'https://www.index.go.kr/post/jibun.jsp',
    #'sec-ch-ua': '"Chromium";v="94", "Google Chrome";v="94", ";Not A Brand";v="99"',
    #'sec-ch-ua-mobile': '?0',
    #'sec-ch-ua-platform': '"Windows"',
    #'Sec-Fetch-Dest': 'empty',
    #'Sec-Fetch-Mode': 'cors',
    #'Sec-Fetch-Site': 'same-origin',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.71 Safari/537.36'
}

index_address_url_path = 'https://www.index.go.kr/post/AjaxRequestXML.jsp'

# http://125.60.46.141/link/search.do?extend=false&mode=jibun_search&searchType=location_jibun&topTab=1&engineCtpNm=%EA%B2%BD%EC%83%81%EB%82%A8%EB%8F%84&engineSigNm=%EC%96%91%EC%82%B0%EC%8B%9C&engineEmdNm=%EB%AC%BC%EA%B8%88%EC%9D%8D&engineLiNm=%EB%B2%94%EC%96%B4%EB%A6%AC&engineBdMaSn=538&engineBdSbSn=&engineMtYn=0&currentPage=1&orgCode=175&orgNm=%ED%86%B5%EA%B3%84%EC%B2%AD%20%ED%99%88%ED%8E%98%EC%9D%B4%EC%A7%80

# http://125.60.46.141/link/search.do?extend=false&mode=jibun_search&searchType=location_jibun&topTab=1&engineCtpNm=경상남도&engineSigNm=양산시&engineEmdNm=물금읍&engineLiNm=범어리&engineBdMaSn=538&engineBdSbSn=&engineMtYn=0&currentPage=1&orgCode=175&orgNm=통계청 홈페이지

get_url_path = 'http://125.60.46.141/link/search.do'
get_url_params = {
    'extend': 'false',
    'mode': 'jibun_search',
    'searchType': 'location_jibun',
    'topTab': '1',
    'engineCtpNm': '경상남도',
    'engineSigNm': '양산시',
    'engineEmdNm': '물금읍',
    'engineLiNm' : '범어리',
    'engineBdMaSn': '538',
    'engineBdSbSn': '',
    'engineMtYn': '0',
    'currentPage': '1',
    'orgCode': '175',
    'orgNm': '통계청 홈페이지',
}

def index_get_address_info(address_jibun):
    result = None

    geturl_url = get_url_path + '?' + parse.urlencode(get_url_params, doseq=True)
    params = {}
    params['getUrl'] = geturl_url
    response = requests.get(index_address_url_path, headers=header, params=params)

    if response.status_code != 200 :
        print(f'Http error : {response.status_code}')
        return result

    #response 데이터 확인
    #print(response.content)

    root = ET.fromstring(response.content.decode('utf-8'))
    for child in root:
        print(child.text)

    return 'Success'

if __name__ == "__main__":
    print(index_get_address_info('4785025324'))
