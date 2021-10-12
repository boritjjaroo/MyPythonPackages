from gov.nsdi.base import Nsdi

# 국가공간정보포털(openapi.nsdi.go.kr)
# 토지특성정보서비스

class LandInfo:

    def __init__(self):
        self.jimok = ''
        self.area = 0.0
        # 도로접면코드
        # https://www.gwanak.go.kr/site/gwanak/standard/Standard_Road_Pop.do
        self.road_side_cd = ''

    def __repr__(self):
        str = f'{self.jimok} {self.area}'
        return str

    @staticmethod
    def search(lawd_cd, is_san, bonbun, bubun, year):
        result = []

        url = f'http://openapi.nsdi.go.kr/nsdi/LandCharacteristicsService/attr/getLandCharacteristics'

        json_data = Nsdi.search(url, lawd_cd, is_san, bonbun, bubun, year)
        root = json_data.get('landCharacteristicss')
        if not root:
            return result
        resultMsg = root.get('resultMsg')
        if resultMsg:
            print(f'landCharacteristicss result message : {resultMsg}')

        list = root.get('field')
        if not list:
            return result

        for item in list:
            land = LandInfo()
            land.jimok = item.get('lndcgrCodeNm', '')
            land.area = float(item.get('lndpclAr', 0.0))
            land.road_side_cd = item.get('roadSideCode', '')
            result.append(land)

        return result


if __name__ == "__main__":
    print(LandInfo.search('4833025321', 0, 510, 3, 2021))
