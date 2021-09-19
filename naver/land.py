# 네이버 부동산
import time
import json
import requests
import os.path
from datetime import datetime, timedelta
from . import map

header = {
#Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9
#Accept-Encoding: gzip, deflate, br
#Accept-Language: ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7
'authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6IlJFQUxFU1RBVEUiLCJpYXQiOjE2MjQ1OTkxMTEsImV4cCI6MTYyNDYwOTkxMX0.r_j2Hf7t1blueIRvXgkEs2yMNiWi1XqJ9SQZpa9Zy0s',
# {"alg":"HS256","typ":"JWT"}
#Cache-Control: max-age=0
#Connection: keep-alive
#Cookie: NNB=RFKYOAM5OONGA; landHomeFlashUseYn=Y; nx_ssl=2; nid_inf=340401216; NID_AUT=b05fI9NFsNgGHy46T5eX/eLxEijYbAXtAadwCapCyK9f2rzfyHwUyv+Jxxk+f8zI; NID_JKL=pk8hbv+ycy6XdDoCQm2jt/ANAbywxe46P9x+rkcWmu8=; nhn.realestate.article.rlet_type_cd=A01; nhn.realestate.article.trade_type_cd=""; NID_SES=AAABm7uyDFw4a9QhHTBB0V05PhwMqYqWuH8fg/mNmzXzU7TB0qob7PLjVocr7ToI8hr+wFeykwIBE3oNsTh7PjMMZr3m6vcaTwykUI2RVfWEGBt3mgOtL0g9YsFR/4EScap0wU880qVoj8yRBUIgu7bw5GP67qi4HxGWUqExmtwF1mAWyUZMIJTxWHPpdyoxLIsWQkMtPI81bycwZvkWjQZzoEZaL5RDhTkbP4dVDMBETp3+bDLplTV+DWcj2Hv6tg7VKBHWsdigaWerZCNOr8kp+z1zDOKO53TJg2LNQZcR3QSmPORyFA7xtNNKMmf+1hJoqHhA7HhWe/vyj+MSf4QKmJaaieHaO16g/VaFJCQoaTHrXxZ2JMizAZSRwoanwnkH9/WcCS0/+QOENRvLTE9m5h9c5sX1qeoxwFY+E3oEQFesY6OUyvUZT9S6KOfAm7/Z1ljmI7vkTgfj28cLB7O5efqi/9iJtpSCOig67B1O5ODIdAG6udv3TglPVSW4Htix75WIiLImgF1VaS7Hog2U+TD/gNfQxDagH5O4+eK7O1WH; realestate.beta.lastclick.cortar=2641000000; SHOW_FIN_BADGE=Y; HT=HM; JSESSIONID=91BF19976F9FAFABC5919FF9407929CD; REALESTATE=1624588385419; wcs_bt=44058a670db444:1624588442
    'Host': 'new.land.naver.com',
#sec-ch-ua: " Not;A Brand";v="99", "Google Chrome";v="91", "Chromium";v="91"
#sec-ch-ua-mobile: ?0
#Sec-Fetch-Dest: document
#Sec-Fetch-Mode: navigate
#Sec-Fetch-Site: none
#Sec-Fetch-User: ?1
#Upgrade-Insecure-Requests: 1
    'Referer': 'https://new.land.naver.com/houses?ms=35.332625,129.006049,17&a=VL:DDDGG:JWJT:SGJT:HOJT&e=RETAIL',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36'
}

# 법정동코드
location_code = {
    '경상남도 양산시 물금읍': '4833025300',
    '경상남도 양산시 동면': '4833031000',
    '경상남도 양산시 원동면': '4833032000',
    '경상남도 양산시 남부동': '4833010200',
    '경상남도 양산시 중부동': '4833010300',
    '경상남도 양산시 북부동': '4833010400',
    '경상남도 양산시 다방동': '4833010100',
    '경상남도 양산시 신기동': '4833010600',
    '경상남도 양산시 북정동': '4833010700',
    '경상남도 양산시 삼호동': '4833011400',
    '경상남도 양산시 명동': '4833011500',
    '경상남도 양산시 평산동': '4833011900',
    '경상남도 양산시 덕계동': '4833012000',
    '경상북도 김천시 율곡동': '4715012000',
    '경상북도 구미시 고아읍': '4719025300',
}

class StringMatchList:
    def __init__(self, match_list) -> None:
        self.match_list = match_list

    def check(self, str):
        for item in self.match_list:
            if 0 <= str.find(item):
                return True
        return False

building_type = {
    '단독/다가구': 'DDDGG',
    '전원주택': 'JWJT',
    '한옥주택': 'HOJT',
    '토지': 'TJ',
}

class InvalidBuildingType(Exception):
    pass

class BuildingType:
    def __init__(self) -> None:
        pass

    def getParamString(type_list):
        result = ''
        for type in type_list:
            type_str = building_type.get(type)
            if type_str is None:
                raise InvalidBuildingType()
            result = result + f':{type_str}'
        return result

pc_list_url = 'https://new.land.naver.com/api/articles'

pc_list_param = {
    'cortarNo': '4833025300',
    'order': 'rank',
    'realEstateType': 'DDDGG',
    'tradeType': 'A1',
    'tag': '::::::::',
    'rentPriceMin': '0',
    'rentPriceMax': '900000000',
    'priceMin': '0',
    'priceMax': '900000000',
    'areaMin': '0',
    'areaMax': '900000000',
    # 사용승인일 00년 이내
    'oldBuildYears': '',
    # 사용승인일 00년 이상
    'recentlyBuildYears': '', 
    'minHouseHoldCount': '', 
    'maxHouseHoldCount': '', 
    'showArticle': 'false',
    'sameAddressGroup': 'false',
    'minMaintenanceCost': '', 
    'maxMaintenanceCost': '', 
    'priceType': 'RETAIL',
    'directions': '', 
    'page': '1',
    'articleState': '' 
}

# https://new.land.naver.com/api/articles/2114363364
pc_detail_url = 'https://new.land.naver.com/api/articles/'

# https://new.land.naver.com/api/article-price-history/2122684815
pc_price_history_url = 'https://new.land.naver.com/api/article-price-history/'

class LandItem:

    def __init__(self):
        self.json_object = None
        self.id = '0'
        self.name = ''
        self.subname = ''
        self.price = 0
        self.description = ''
        self.detailDescription = ''
        self.confirm_day = ''
        # 건축물대장 - 사용승인일
        self.use_approve_day = ''
        # 부동산입력 - 사용승인일
        self.use_approve_day2 = ''
        self.all_ho_count = 0
        self.address = ''
        self.is_location_address = False
        self.ground_floor_count = 0
        self.underground_floor_count = 0
        self.area = 0
        self.building_area = 0
        self.total_floor_area = 0

        self.initial_price = ''

        self.is_new = False
        self.is_favorite = False
        self.is_multi_family = None
        self.build_years = None

    @staticmethod
    def getJsonFileNameS(article_no, article_confirm_ymd):
        file_name = f'{article_no}-{article_confirm_ymd}.json'
        return file_name

    @staticmethod
    def createFromJson(json_path, article_no, article_confirm_ymd):
        item = LandItem()
        json_path = f'{json_path}/{item.getJsonFileNameS(article_no, article_confirm_ymd)}'
        item.loadJson(json_path)
        return item

    def getJsonFileName(self):
        return self.getJsonFileNameS(self.id, self.confirm_day)

    def parseFromJson(self, json_object):
        if json_object.get('articleDetail') is not None:
            self.id = json_object['articleDetail'].get('articleNo')
            self.name = json_object['articleDetail'].get('articleName')
            self.subname = json_object['articleDetail'].get('articleSubName')
            self.confirm_day = json_object['articleDetail'].get('articleConfirmYMD')
            self.description = json_object['articleDetail'].get('articleFeatureDescription')
            self.detailDescription = json_object['articleDetail'].get('detailDescription')

        if json_object.get('articlePrice') is not None:
            self.price = json_object['articlePrice'].get('dealPrice')

        if json_object.get('articleFacility') is not None:
            self.use_approve_day2 = json_object['articleFacility'].get('buildingUseAprvYmd')

        if json_object.get('articleBuildingRegister') is not None:
            self.use_approve_day = json_object['articleBuildingRegister'].get('useAprDay')
            self.all_ho_count = json_object['articleBuildingRegister'].get('allHoCnt')
            if str(type(self.all_ho_count)) != "<class 'int'>":
                self.all_ho_count = int(self.all_ho_count)
            self.address = json_object['articleBuildingRegister'].get('platPlc')
            self.ground_floor_count = json_object['articleBuildingRegister'].get('grndFlrCnt')
            self.underground_floor_count = json_object['articleBuildingRegister'].get('ugrndFlrCnt')
            self.area = json_object['articleBuildingRegister'].get('platArea')
            self.building_area = json_object['articleBuildingRegister'].get('archArea')
            self.total_floor_area = json_object['articleBuildingRegister'].get('totArea')
        elif json_object.get('articleSpace') is not None:
            self.area = json_object['articleSpace'].get('groundSpace')

        if self.address is None or len(self.address) == 0:
            longitude = json_object['articleDetail'].get('longitude')
            latitude = json_object['articleDetail'].get('latitude')
            address_dic = map.coords_to_addr(longitude, latitude)
            address_addr = map.coords_to_addr(longitude, latitude).get('addr')
            if len(address_dic) == 0:
                self.address = f"{latitude} {longitude}"
            elif address_addr is not None:
                self.address = address_addr
            else:
                self.address = address_dic.values()[0]
            self.is_location_address = True

    def getPriceHistory(self):
        url = f'{pc_price_history_url}{self.id}'
        response = requests.get(url, headers=header)

        if response.status_code != 200 :
            print(f'Http error : {response.status_code}')
            return

        #response 데이터 확인
        #print(response.content)

        json_object = json.loads(response.content)

        self.initial_price = json_object.get('initialPrice', '')

    def parseFromID(self, id_str):
        url = f'{pc_detail_url}{id_str}'
        response = requests.get(url, headers=header)

        if response.status_code != 200 :
            print(f'Http error : {response.status_code}')
            return

        #response 데이터 확인
        #print(response.content)

        json_object = json.loads(response.content)
        #print(json_detail)

        self.json_object = json_object
        self.parseFromJson(json_object)

    def loadJson(self, file_path):
        if os.path.isfile(file_path) == False:
            return False
        with open(file_path, 'r', encoding='utf-8') as json_file:
            json_object = json.load(json_file)
        self.parseFromJson(json_object)
        return True
        
    def saveJson(self, path):
        file_path = f'{path}/{self.getJsonFileName()}'
        if os.path.isfile(file_path):
            return
        with open(file_path, 'w', encoding='utf-8') as out_file:
            json.dump(self.json_object, out_file, indent=4, ensure_ascii=False)
            print(f'{file_path} saved.')
        return

    def calcBuildYears(self):
        time_build = None
        # 부동산 입력 정보 우선 적용
        if self.use_approve_day2:
            print(self.use_approve_day2)
            year = int(self.use_approve_day2[0:4])
            month = int(self.use_approve_day2[4:6])
            month = max([month, 1])
            day = int(self.use_approve_day2[6:8])
            day = max([day, 1])
            time_build = datetime(year, month, day)
        # 부동산 입력 정보가 없을 경우 건축물대장 정보 적용
        elif self.use_approve_day:
            print(self.use_approve_day)
            numbers = self.use_approve_day.split('.')
            if len(numbers) == 1:
                time_build = datetime(int(numbers[0]), 1, 1)
            elif len(numbers) == 2:
                time_build = datetime(int(numbers[0]), int(numbers[1]), 1)
            elif len(numbers) == 3:
                time_build = datetime(int(numbers[0]), int(numbers[1]), int(numbers[2]))

        if time_build:
            self.build_years = round((datetime.now() - time_build).days / 365, 1)
        else:
            self.build_years = None

    def prettyPrint(self):
        print(f'{self.id}  {self.name}  {self.price}  {self.use_approve_day}   {self.address}')


class LandListItem:
    def __init__(self):
        self.articleNo = ''
        self.articleName = ''
        self.articleConfirmYmd = ''
        self.latitude = ''
        self.longitude = ''

class LandListCrawler:

    def __init__(self):
        self.save_path = '.'
        self.name_except_filter = StringMatchList([])
        self.param_building_type = ''
        self.param_oldBuildYears = ''
        self.param_recentlyBuildYears = ''

    def setSavePath(self, save_path):
        self.save_path = save_path

    def setNameExceptFilter(self, except_list):
        self.name_except_filter = StringMatchList(except_list)

    def setBuildingType(self, type_list):
        param_str = None
        for type in type_list:
            if param_str is None:
                param_str = type
            else:
                param_str = f'{param_str}:{type}'
        self.param_building_type = param_str

    def setWithinYears(self, oldBuildYears, recentlyBuildYears):
        self.param_oldBuildYears = oldBuildYears
        self.param_recentlyBuildYears = recentlyBuildYears

    def parse(self, locationCode, page):
        is_more_data = False
        result_list = []

        url = pc_list_url
        param = pc_list_param

        param.update(cortarNo=locationCode)
        param.update(realEstateType=self.param_building_type)
        param.update(oldBuildYears=self.param_oldBuildYears)
        param.update(recentlyBuildYears=self.param_recentlyBuildYears)
        param.update(page=page)

        print(f'page : {page}')
        print(param)
        response = requests.get(url, params=param, headers=header)

        if response.status_code == 200 :
            #response 데이터 확인
            #print(response.content)

            try:
                json_data = json.loads(response.content)
                #print(json_data)

                is_more_data = json_data['isMoreData']
                items = json_data['articleList']
                item_count = len(items)
                print(f'목록 개수 : {item_count}')

                for item in items :
                    list_item = LandListItem()
                    list_item.articleNo = item["articleNo"]
                    list_item.articleName = item['articleName']
                    list_item.articleConfirmYmd = item['articleConfirmYmd']
                    list_item.latitude = item['latitude']
                    list_item.longitude = item['longitude']

                    # 진행률 표시
                    print(f'{list_item.articleNo} : ', end='')

                    # 이름으로 필터링해서 제외시킴
                    if self.name_except_filter.check(list_item.articleName):
                        print(f'{list_item.articleName} filtered.')
                        continue

                    result_list.append(list_item)
                    print('found.')
            except:
                print('LandListCrawler::parse() exception occured.')

        else:
            print(f'Http error : {response.status_code}')

        return is_more_data, result_list


if __name__ == "__main__":
    rs = LandItem()
    rs.parseFromID('2114476497')
    rs.prettyPrint()
    print(rs.json_object)
    #rs.saveJson('.')
