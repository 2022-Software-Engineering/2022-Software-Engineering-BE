import urllib

from rest_framework.response import Response
from rest_framework.views import APIView
import secret
import requests
import xmltodict as xmltodict
from rest_framework.utils import json


def requestPlantList(params):
    # open api url
    url = 'http://api.nongsaro.go.kr/service/dryGarden/dryGardenList'

    # open api request
    response = requests.get(url, params=params)

    # xml to json
    xpars = xmltodict.parse(response.text)
    jsonDump = json.dumps(xpars)
    jsonBody = json.loads(jsonDump)

    result_list = list()
    items = jsonBody['response']['body']['items']['item']
    print(items)
    print(len(items))
    print(len(jsonBody['response']['body']['items']))
    print("a")
    print(jsonBody['response']['body']['items'])
    for item in items:
        r = {}
        r['plantID'] = item['cntntsNo']
        r['plantNameKR'] = item['cntntsSj']
        r['plantNameEN'] = item['scnm']
        r['plantImgUrl'] = item['imgUrl1']
        result_list.append(r)

    return result_list

def requestPlantDetails(plantID):
    # open api url
    url = 'http://api.nongsaro.go.kr/service/dryGarden/dryGardenDtl'

    params = {'apiKey': secret.key, 'cntntsNo': plantID }

    # open api request
    response = requests.get(url, params=params)

    # xml to json
    xpars = xmltodict.parse(response.text)
    jsonDump = json.dumps(xpars)
    jsonBody = json.loads(jsonDump)

    r = {}
    item = jsonBody['response']['body']['item']
    r['plantID'] = item['cntntsNo']
    r['plantNameKR'] = item['cntntsSj']
    r['plantNameEN'] = item['scnm']
    r['plantImgUrl'] = item['mainImgUrl1']
    r['plantDescription'] = item['clCodeDc']
    r['countryOfOrigin'] = item['orgplce']
    r['flowerExist'] = item['flwrInfo']
    r['characteristic'] = item['chartrInfo']
    r['rootForm'] = item['rdxStleNm']
    r['growthPattern'] = item['grwtInfo']
    r['growthRate'] = item['grwtseVeNm']
    r['lightAmount'] = item['lighttInfo']
    r['watering'] = item['waterCycleInfo']
    r['demangeOfBugs'] = item['dlthtsInfo']
    r['manageLevel'] = item['manageLevelNm']
    r['manageDemand'] = item['manageDemandNm']
    r['fertilizer'] = item['frtlzrInfo']
    r['placeOfDeployment'] = item['batchPlaceInfo']
    r['plantingTip'] = item['tipInfo']

    return r

# 검색, 추천, 필터링 결과 요청 api
class SearchResultList(APIView):
    def get(self, request):
        # 요청변수
        _searchType = request.query_params.get('searchType') # 사용자 선택 검색 언어
        _searchWord = urllib.parse.unquote(request.query_params.get('searchWord')) # 사용자 입력 검색어
        _growRate = request.query_params.get('growRate') # 사용자 선택 생장 속도
        _manageLevel = request.query_params.get('manageLevel') # 사용자 선택 관리 수준
        _manageDemand = request.query_params.get('manageDemand') # 사용자 선택 관리 요구도

        #parameter들, 사용자가 입력한 검색 조건으로만 parameter를 생성함
        params = {}
        params['apiKey'] = secret.key

        if _searchType != '0':
            params['sType'] = _searchType

        if _searchWord != '0':
            params['sText'] = _searchWord

        if _growRate != '0':
            params['grwtseVeCodeVal'] = _growRate

        if _manageLevel != '0':
            params['manageLevelCodeVal'] = _manageLevel

        if _manageDemand != '0':
            params['manageDemandCodeVal'] = _manageDemand

        print(params)
        #openAPI 요청
        result_list = requestPlantList(params)

        # 검색 결과가 있는 경우 해당 결과들이 추가된 리스트 return
        if result_list:
            return Response(result_list)

        #검색  결과가 없는 경우 None을 return
        return Response({
            "returnCode": "None"
        })


class PlantDetails(APIView):
    def get(self, request):
        _plantID = request.query_params.get('plantID')

        plantDetails = requestPlantDetails(_plantID)

        if plantDetails:
            return Response(plantDetails)

        return Response({
            "returnCode": "None"
        })
        return Response({"d":"d"})