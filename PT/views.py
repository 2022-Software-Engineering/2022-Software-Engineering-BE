import secret
import requests
import urllib

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.utils import json
import xmltodict as xmltodict

from .models import User, InterestPlant


def targetStrRemover(str):
    target = ['<br />', '<br/>']
    if str is None:
        return str
    for t in target:
        str = str.replace(t, '')
    return str

# 사용자가 선택한 검색조건으로 parmas 매개변수를 받아 open API 요청
def requestPlantList(params):
    # open api url
    url = 'http://api.nongsaro.go.kr/service/dryGarden/dryGardenList'
    # open api request
    response = requests.get(url, params=params)
    # xml to json
    xpars = xmltodict.parse(response.text)
    jsonDump = json.dumps(xpars)
    jsonBody = json.loads(jsonDump)
    # parsing
    totalCount = jsonBody['response']['body']['items']['totalCount']

    result_list = list()
    # 검색 결과 수가 0인 경우 빈 return_list return
    if totalCount != '0':
        items = jsonBody['response']['body']['items']['item']
        # 검색 결과 수가 1인 경우
        if totalCount == '1':
            r = {}
            r['plantID'] = items['cntntsNo'] # 식물 ID
            r['plantNameKR'] = items['cntntsSj'] # 식물명(한글)
            str = items['scnm'] # 식물명(영어)
            new_str = str.replace('<i>', '')
            new_str = new_str.replace('</i>', '')
            r['plantNameEN'] = new_str
            r['plantImgUrl'] = items['imgUrl1'] # 식물 img
            result_list.append(r)
        # 검색 결과 수가 2 이상인 경우
        else:
            for item in items:
                r = {}
                r['plantID'] = item['cntntsNo'] # 식물 ID
                r['plantNameKR'] = item['cntntsSj'] # 식물명(한글)
                str = item['scnm']  # 식물명(영어)
                new_str = str.replace('<i>', '')
                new_str = new_str.replace('</i>', '')
                r['plantNameEN'] = new_str
                r['plantImgUrl'] = item['imgUrl1']
                result_list.append(r)
        return result_list

    return result_list

# 식물 상세 정보 OPEN API 요청
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

    resultCode = jsonBody['response']['header']['resultCode']
    # 상세 정보가 없는 경우(잘못된 plantID로 요청보낸 경우)
    r={}
    if resultCode == '91':
        return r
    else:
        item = jsonBody['response']['body']['item']

        r['plantID'] = item['cntntsNo'] #식물 ID
        r['plantNameKR'] = item['cntntsSj'] #식물명(한글)
        str = item['scnm']  # 식물명(영어)
        new_str = str.replace('<i>', '')
        new_str = new_str.replace('</i>', '')
        r['plantNameEN'] = new_str
        r['plantImgUrl'] = item['mainImgUrl1'] #식물 img
        r['plantDescription'] =item['clCodeDc'] #과 설명
        r['countryOfOrigin'] = item['orgplce'] #원산지
        r['flowerExist'] = item['flwrInfo'] #꽃
        r['characteristic'] = targetStrRemover(item['chartrInfo']) #특성
        r['rootForm'] = item['rdxStleNm'] #뿌리형태
        r['growthPattern'] = item['grwtInfo'] #생장형
        r['growthRate'] = item['grwtseVeNm'] #생장속도
        r['lightAmount'] = targetStrRemover(item['lighttInfo']) #광
        r['watering'] = targetStrRemover(item['waterCycleInfo']) #물주기
        r['demangeOfBugs'] = item['dlthtsInfo'] #병충해
        r['manageLevel'] = item['manageLevelNm'] #관리수준
        r['manageDemand'] = item['manageDemandNm'] #관리요구도
        r['fertilizer'] = item['frtlzrInfo'] #비료
        r['placeOfDeployment'] = targetStrRemover(item['batchPlaceInfo']) # 배치 장소
        r['plantingTip'] = item['tipInfo'] #팁

    return r

# 검색, 추천, 필터링 결과 요청 api
class SearchResultList(APIView):
    def get(self, request):
        # 요청변수
        _searchType = request.data.get('searchType') # 사용자 선택 검색 언어
        _searchWord = urllib.parse.unquote(request.data.get('searchWord')) # 사용자 입력 검색어
        _growRate = request.data.get('growRate') # 사용자 선택 생장 속도
        _manageLevel = request.data.get('manageLevel') # 사용자 선택 관리 수준
        _manageDemand = request.data.get('manageDemand') # 사용자 선택 관리 요구도

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

        #openAPI 요청
        result_list = requestPlantList(params)

        # 검색 결과가 있는 경우 해당 결과들이 추가된 리스트 return
        if result_list:
            return Response(result_list)
        #검색  결과가 없는 경우 None을 return
        return Response({
            "returnCode": "None"
        })

# 상세 정보 요청 API
class PlantDetails(APIView):
    def get(self, request):
        _plantID = request.data.get('plantID')
        # open API 요청
        plantDetails = requestPlantDetails(_plantID)

        # 상세 정보 조회 결과가 있는 경우 해당 결과들이 추가된 리스트 return
        if plantDetails:
            return Response(plantDetails)
        #검색  결과가 없는 경우 None을 return
        return Response({
            "returnCode": "None"
        })

# login API
class Login(APIView):
    def post(self, request):
        userID = request.data.get('userID')
        password = request.data.get('password')

        try:
            user = User.objects.get(userID=userID)
        except User.DoesNotExist:
            return Response({'isLogined': 'Fail'})

        if user.userPW == password:
            return Response({'isLogined': 'Success'})

        return Response({'isLogined': 'Fail'})

# 관심식물 등록 api
class RegisterInterest(APIView):
    def post(self, request):
        _userID = request.data.get('userID')
        _plantID = request.data.get('plantID')

        # user가 존재하지 않는 경우
        try:
            user = User.objects.get(userID=_userID)
        except User.DoesNotExist:
            return Response({'returnCode': 'NoneUser'})

        try:
            InterestPlant.objects.create(
                userID=user,
                plantID=_plantID
            )
        except :
            #중복된 값인 경우
            return Response({'returnCode': 'DuplicatedData'})

        return Response({'returnCode': 'Success'})


class InterestPlantList(APIView):
    def post(self, request):
        _userID = request.data.get('userID')

        # user가 존재하지 않는 경우 - api 테스트시 사용
        try:
            user = User.objects.get(userID=_userID)
        except User.DoesNotExist:
            return Response({'returnCode': 'NoneUser'})

        IP_list = InterestPlant.objects.filter(userID=_userID)

        result_list = []
        if IP_list:
            for item in IP_list:
                plantDetails = requestPlantDetails(item.plantID)
                result_list.append(plantDetails)

        return Response(result_list)