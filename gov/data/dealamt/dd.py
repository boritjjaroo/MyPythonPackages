import requests

# 공공데이터포털(data.go.kr)
# 국토교통부_단독/다가구 매매 실거래 자료

class DealAmountDD:

    def __init__(self):
        pass

    def __repr__(self):
        str = f''
        return str

    @staticmethod
    def search(lawd_cd, date):
        result = []

        url = 'http://openapi.molit.go.kr:8081/OpenAPI_ToolInstallPackage/service/rest/RTMSOBJSvc/getRTMSDataSvcSHTrade'
        params = {
            #'serviceKey': 'qfQojagnysTVPmjT1uqI%2FfKsnPs%2FWc5MG%2BYbocnb%2FIun1%2Fjrnq4PQ1uz7JcqWvShL%2FpIbmRIdlKCcHMUYqsU5g%3D%3D',
            'serviceKey': 'qfQojagnysTVPmjT1uqI/fKsnPs/Wc5MG+Ybocnb/Iun1/jrnq4PQ1uz7JcqWvShL/pIbmRIdlKCcHMUYqsU5g==',
            # 5자리
            'LAWD_CD': '48330',
            'DEAL_YMD': '202109',
        }

        response = requests.get(url, params=params)
        if response.status_code != 200 :
            print(f'Http error : {response.status_code}')
            return result

        #response 데이터 확인
        print(response.content)


if __name__ == "__main__":
    print(DealAmountDD.search('4833025300', '2021-09-01'))
