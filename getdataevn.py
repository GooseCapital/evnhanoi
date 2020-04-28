import requests
import xmltodict


def getData(customerid, year):
    url = 'http://42.112.213.225:8050/Service.asmx/get_hdon_tracuu'
    headers = {'Host': '42.112.213.225',
               'Accept-Language': 'en-us',
               'User-Agent': 'EVNHANOI20CSKH/4.1.1 CFNetwork/976 Darwin/18.2.0'}
    body = {'ma_kh': customerid,
            'nam': year,
            'thang': '1',
            'thangsau': '12'}
    r = requests.post(url, data=body, headers=headers)
    result = xmltodict.parse(r.text)
    allData = []
    try:
        for monthData in result['DataTable']['diffgr:diffgram']['NewDataSet']['SMS05']:
            allData.append({'customerId': monthData['MA_KHANG'],
                            'month': monthData['THANG'],
                            'year': monthData['NAM'],
                            'power': monthData['SAN_LUONG'],
                            'totalMoney': '{:,.0f}'.format(int(monthData['TONG_TIEN']))})
    except:
        allData.append({'customerId': customerid,
                        'month': "Không có thông tin",
                        'year': "Không có thông tin",
                        'power': "Không có thông tin",
                        'totalMoney': "Không có thông tin"})
    return allData


def getlastestmonth(customerid, year):
    allData = getData(customerid, year)
    return allData[len(allData) - 1]
