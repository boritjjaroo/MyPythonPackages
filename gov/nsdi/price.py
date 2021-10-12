from gov.nsdi.base import Nsdi

# 국가공간정보포털(openapi.nsdi.go.kr)
# 개별주택가격속성조회

class HousePrice:

    def __init__(self):
        self.area_t = 0.0
        self.area_e = 0.0
        self.total_area_t = 0.0
        self.total_area_e = 0.0
        self.price = 0
        self.date = None

    def __repr__(self):
        str = f'가격:{self.price} 날짜:{self.date}'
        return str

    @staticmethod
    def search(lawd_cd, is_san, bonbun, bubun, year):
        result = []

        url = f'http://openapi.nsdi.go.kr/nsdi/IndvdHousingPriceService/attr/getIndvdHousingPriceAttr'

        json_data = Nsdi.search(url, lawd_cd, is_san, bonbun, bubun, year)
        root = json_data.get('indvdHousingPrices')
        if not root:
            return result
        resultMsg = root.get('resultMsg')
        if resultMsg:
            print(f'indvdHousingPrices result message : {resultMsg}')

        list = root.get('field')
        if not list:
            return result

        for item in list:
            building = HousePrice()
            building.area_t = float(item.get('ladRegstrAr', 0.0))
            building.area_e = float(item.get('calcPlotAr', 0.0))
            building.total_area_t = float(item.get('buldAllTotAr', 0.0))
            building.total_area_e = float(item.get('buldCalcTotAr', 0.0))
            building.price = int(item.get('housePc', 0))
            std_year = item.get('stdrYear')
            std_month = item.get('stdrMt')
            building.date = f'{std_year}-{std_month}-01'
            result.append(building)

        return result


if __name__ == "__main__":
    print(HousePrice.search('4833025324', 0, 508, 14, 2021))
