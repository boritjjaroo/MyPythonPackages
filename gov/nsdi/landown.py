from gov.nsdi.base import Nsdi

# 국가공간정보포털(openapi.nsdi.go.kr)
# 토지소유정보속성조회

class LandOwn:

    def __init__(self):
        self.cause = ''
        # 'yyyy-mm-dd'
        self.change_date = ''
        self.update_date = ''

    def __repr__(self):
        str = f'{self.cause} {self.change_date} {self.update_date}'
        return str

    @staticmethod
    def search(lawd_cd, is_san, bonbun, bubun):
        result = []

        url = f'http://openapi.nsdi.go.kr/nsdi/PossessionService/attr/getPossessionAttr'

        json_data = Nsdi.search(url, lawd_cd, is_san, bonbun, bubun)
        root = json_data.get('possessions')
        if not root:
            return result
        resultMsg = root.get('resultMsg')
        if resultMsg:
            print(f'possessions result message : {resultMsg}')

        list = root.get('field')
        if not list:
            return result

        for item in list:
            land = LandOwn()
            land.cause = item.get('ownshipChgCauseCodeNm', '')
            land.change_date = item.get('ownshipChgDe', '')
            land.update_date = item.get('lastUpdtDt', '')
            result.append(land)

        return result


if __name__ == "__main__":
    print(LandOwn.search('4833025324', 0, 721, 15))
