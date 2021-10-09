# 네이버 맵 API
import json
import requests


# 네이버맵에서 좌표로 주소 구하는 URL
# 원본 : https://map.naver.com/v5/api/geocode?request=coordsToaddr&version=1.0&sourcecrs=epsg:4326&output=json&orders=addr,roadaddr&coords=128.3660622,36.1432817
# https://map.naver.com/v5/api/geocode?request=coordsToaddr&output=json&orders=addr&coords=128.3660622,36.1432817
api_url_coords_to_addr = 'https://map.naver.com/v5/api/geocode?request=coordsToaddr&output=json&orders=addr,roadaddr&coords='

header = {
    #accept: application/json, text/plain, */*
    #accept-encoding: gzip, deflate, br
    #accept-language: ko-KR,ko;q=0.8,en-US;q=0.6,en;q=0.4
    #cache-control: no-cache
    #content-type: application/json
    #cookie: NNB=RFKYOAM5OONGA; nx_ssl=2; nid_inf=340401216; NID_AUT=b05fI9NFsNgGHy46T5eX/eLxEijYbAXtAadwCapCyK9f2rzfyHwUyv+Jxxk+f8zI; NID_JKL=pk8hbv+ycy6XdDoCQm2jt/ANAbywxe46P9x+rkcWmu8=; csrf_token=d7537dedb0e44e65939e745d1d73fea007d97ba67fb0671bc24fa5d02cebcdeb22c92feb150f3f4dddb685bc32204e28379ebd06956a7c9690a2dce8ee819f70; NID_SES=AAABmE9CVcWOrbfMnGpwnY7FicoGwh2GxHYjuhMgQNBirK8DRsYFXylmciFfRTK01o8cns611+bKX3b0HNYo2t62GXdhQUEOvcoORxr5kXyl/t6NKVukEHB5bW1+OGdiaMSFqsvaUQGzeAhYHX/m+EbERtOgJP0J62F+VAyOKgwl2PXshFBIMj6x53EPqH++yWkt+FAUZUvjhNcif9vF44n4v+7pZPNzoEN4anVF/YN4SiI9gmwSgYON4iT4udduCq735btELj3wM8LAMq5V6Pu9XVCWru6TIa4NhAPsoFOIraYocM9XWA9HNoV8AxvGXzhr4JUZs96U3gEL2bO5/CtyLzIJq/HBqhnaJi5X82Cuw+XEJ3zKYXn8WK0eDQo9Cf7FXpnwUzSrDoseui1uXA+S9BXjotSyPnqy+CLavKC/X8cZM9d+txQJvgDwPQFXP35wImvAz3m3QdoBNB3bRpOEPkNM9v4ZXxvjMaP4djQ4vggT4uzbovkKRsbg1kBQpMBoAMOaY0UjKrnyxkFCtBL72DVQddOpPA8ThgGWeZMjhL+Q; page_uid=e458388c-bc83-4f2a-9c75-2c2e285aac74
    #expires: Sat, 01 Jan 2000 00:00:00 GMT
    #pragma: no-cache
    'referer': 'https://map.naver.com/',
    #sec-ch-ua: " Not;A Brand";v="99", "Google Chrome";v="91", "Chromium";v="91"
    #sec-ch-ua-mobile: ?0
    #sec-fetch-dest: empty
    #sec-fetch-mode: cors
    #sec-fetch-site: same-origin
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36',
}

def coords_to_addr(longitude, latitude):
    address = {}

    url = f'{api_url_coords_to_addr}{longitude},{latitude}'
    response = requests.get(url, headers=header)

    if response.status_code != 200 :
        print(f'Http error : {response.status_code}')
        return address

    #response 데이터 확인
    #print(response.content)

    json_data = json.loads(response.content)
    #print(json_data)

    if json_data['status']['code'] != 0:
        print(f"Naver error : {json_data['status']['name']}")
        return address
    
    json_results = json_data['results']
    if len(json_results) == 0:
        print(f"can't found address.")
        return address

    for json_result in json_results:
        key = json_result['name']
        value = ''

        json_region = json_result['region']
        if json_region is None:
            print('Naver error : json data invalid')
            continue
        
        if json_region['area1'] is not None:
            value = f"{value} {json_region['area1']['name']}"
        if json_region['area2'] is not None:
            value = f"{value} {json_region['area2']['name']}"
        if json_region['area3'] is not None:
            value = f"{value} {json_region['area3']['name']}"
        if json_region['area4'] is not None:
            value = f"{value} {json_region['area4']['name']}"

        json_land = json_result['land']
        if json_land is None:
            print('Naver error : json data invalid')
            continue

        if json_land.get('name') is not None:
            value = f"{value} {json_land['name']}"
        if json_land['number1'] is not None:
            value = f"{value} {json_land['number1']}"
        if json_land['number2'] is not None:
            value = f"{value}-{json_land['number2']}"

        address[key] = value

    return address


# 네이버맵에서 주소 검색 URL
# 원본 : https://map.naver.com/v5/api/search?caller=pcweb&query=경상남도 양산시 동면 금산리 1434-12번지&type=all&searchCoord=129.02129840000026;35.311907900000186&page=1&displayCount=20&isPlaceRecommendationReplace=true&lang=ko
api_url_addr_search = 'https://map.naver.com/v5/api/search?query='

header = {
    #accept: application/json, text/plain, */*
    #accept-encoding: gzip, deflate, br
    #accept-language: ko-KR,ko;q=0.8,en-US;q=0.6,en;q=0.4
    #cache-control: no-cache
    #content-type: application/json
    #cookie: NNB=RFKYOAM5OONGA; NID_JKL=pk8hbv+ycy6XdDoCQm2jt/ANAbywxe46P9x+rkcWmu8=; NID_AUT=6xLSgMNx8xu9+yr5HfYDa/d2FPEnM8bQ8YE5xHP40wdpElok3UyNXmzPKe0+KCIq; NFS=2; page_uid=hgkOwlpw8DNssdTv5Jwssssssss-099643; csrf_token=3cd8c9bafd7c327bc818b12fb42b3077bf76aa9a9ec5bd0699a8167c84398e911f36c132f78a2179b049d8a5db4e7e73867634dae21e673f2b7f22ba25c19ce2; BMR=s=1633494397471&r=https%3A%2F%2Fm.blog.naver.com%2Fhankrah%2F221755651815&r2=https%3A%2F%2Fwww.google.com%2F; NID_SES=AAABluSux5x2u7q/ETBJLkInIKRSVHahbwKTHgBsasxH+Yr6V05K5wMkYBYGzzJuIGWDdGLgsPmtYXxKZ4dwLwG0s+sHLGs6g53kY9SMZXo+ZFoa1/6bJ3fS/wXbz5zRdk3bhSJhvFn5sACvCCaXk5doWdZMsNFOP0N5E8p4JWrQh17Y4NpE5z+c2hfZO5jn0ONAFeW4DNFeA39kEHR7cM8rOq2TO8RnTiIXaabOuc7CZrjPrwuDHlMPCWW5LvQ/h+qQ9Q6Vk5J/+kGt/zyGf997e7APV4zDiklV0ZmRZWYFQGlq8T30slPhQUCjfEePKNYpNX+Ld427LJCJAlApVSgfn0/gNTZy7tBlgY/YMdoqkxbLu9wnv4dTDBuXm2v+2xT7nns/8bB8kPdEDRLy6qBqncrbuTUPOGJNEu/rwHtkaYtf8y1+JStUa/9w4noiAl+YD7HyNpBvQJLdfHEODwSsKhMwbgXgNXqIMKpt0kKKHzEFhspLHGfVeURYfhvzDo+ZfSDvcF0gzRWH3jwt3b7GbEeQbupTgOlvfCtki3vJddDB; page_uid=3850d49c-04eb-4187-8277-13c7e6d5bc7a
    #expires: Sat, 01 Jan 2000 00:00:00 GMT
    #pragma: no-cache
    'referer': 'https://map.naver.com/',
    #sec-ch-ua: "Chromium";v="94", "Google Chrome";v="94", ";Not A Brand";v="99"
    #sec-ch-ua-mobile: ?0
    #sec-ch-ua-platform: "Windows"
    #sec-fetch-dest: empty
    #sec-fetch-mode: cors
    #sec-fetch-site: same-origin
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36',
}

class AddressInfo:
    def __init__(self):
        self.address_road = ''
        self.lawd_cd = ''
        self.jibun = ''

    def __str__(self) -> str:
        return str(self.address_road)

def addr_search(search_address):
    url = f'{api_url_addr_search}{search_address}'
    response = requests.get(url, headers=header)

    if response.status_code != 200 :
        print(f'Http error : {response.status_code}')
        return None

    #response 데이터 확인
    #print(response.content)

    json_data = json.loads(response.content)
    #print(json.dumps(json_data, indent=4, ensure_ascii=False))

    info = AddressInfo()

    address_list = json_data['result']['address']['jibunsAddress']['list']
    if address_list[0].get('mappedAddress'):
        info.address_road = address_list[0]['mappedAddress']['fullAddress']
    info.lawd_cd = address_list[0]['addressElements']['bcode']
    info.jibun = address_list[0]['addressElements']['jibun']

    return info

# IP로 위치 찾기
# https://map.naver.com/v5/api/gloc?ip=211.213.235.44&ntype=Y&ext=y&ncodetype=all
api_url_ip_to_addr_format = 'https://map.naver.com/v5/api/gloc?ip={0}&ntype=Y&ext=y&ncodetype=all'

def ip_to_addr(ip_str):
    result_list = []
    url = api_url_ip_to_addr_format.format(ip_str)
    response = requests.get(url, headers=header)

    if response.status_code != 200 :
        print(f'Http error : {response.status_code}')
        return result_list

    #response 데이터 확인
    #print(response.content)

    json_data = json.loads(response.content)
    #print(json_data)

    json_gloc = json_data['gloc']

    for json_item in json_gloc:
        result_dic = {}
        result_dic['address'] = f"{json_item['r1']} {json_item['r2']} {json_item['r3']}"
        result_dic['latitude'] = json_item['lat']
        result_dic['longitude'] = json_item['long']
        result_dic['accuracy'] = json_item['accuracy']
        result_list.append(result_dic)

    return result_list


if __name__ == "__main__":
    print(addr_search('경상남도 양산시 물금읍 물금리 434번지'))
    print(coords_to_addr('128.3660622', '36.1432817'))
    print(ip_to_addr('211.213.235.44'))
