from gov.nsdi.base import Nsdi

# 국가공간정보포털(openapi.nsdi.go.kr)
# 용도별건물속성조회

class BuildingInfo(Nsdi):

    def __init__(self):
        self.plot_area = 0.0
        self.building_area = 0.0
        self.building_total_area = 0.0
        self.structure = ''
        self.main_purpose = ''
        self.detail_purpose = ''
        self.building_purpose = ''
        self.height = 0.0
        self.ground_floor = 0
        self.under_floor = 0
        # 'yyyy-mm-dd'
        self.use_date = ''
        # 'yyyy-mm-dd'
        self.update_date = ''

    def __repr__(self):
        str = f'대지:{self.plot_area}'
        return str

    @staticmethod
    def search(lawd_cd, is_san, bonbun, bubun):
        result = []

        url = f'http://openapi.nsdi.go.kr/nsdi/BuildingUseService/attr/getBuildingUse'

        json_data = Nsdi.search(url, lawd_cd, is_san, bonbun, bubun)
        root = json_data.get('buildingUses')
        if not root:
            return result
        resultMsg = root.get('resultMsg')
        if resultMsg:
            print(f'buildingUses result message : {resultMsg}')

        list = root.get('field')
        if not list:
            return result

        for item in list:
            building = BuildingInfo()
            building.plot_area = float(item.get('buldPlotAr', 0.0))
            result.append(building)

        return result


if __name__ == "__main__":
    print(BuildingInfo.search('4833025324', 0, 508, 14))
    print(BuildingInfo.search('4833025324', 0, '508', ''))
