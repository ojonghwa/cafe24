from rest_framework import viewsets, generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import CreateAPIView

# from rest_framework.pagination import LimitOffsetPagination
# Django REST framework JWT: JSON Web Token Authentication

from rest_framework.authentication import (
    BasicAuthentication,
    TokenAuthentication,
    SessionAuthentication,
)
from rest_framework.permissions import (
    IsAuthenticated,
    IsAdminUser,
    IsAuthenticatedOrReadOnly,
    AllowAny,
)
from django.contrib.auth import authenticate
from rest_framework.status import (
    HTTP_404_NOT_FOUND,
    HTTP_400_BAD_REQUEST,
    HTTP_200_OK,
    HTTP_201_CREATED,
)
from rest_framework.authtoken.models import Token

from shop.models import Product, Category
from blog.models import Post, Comment
from orders.models import Order, OrderItem
from django.contrib.auth.models import User
from .serializers import (
    ProductSerializer,
    CategorySerializer,
    CategoryProductSerializer,
    OrderSerializer,
    OrderItemSerializer,
    PostSerializer,
    UserSerializer,
    SignupSerializer,
)
from django.db.models import Q
import sys, requests
from cafe24.settings import KoreaApiKey2, CoronaApiKey, WeatherApiKey

# from rest_framework.decorators import api_view
from iot.models import Esp8266
from xml.etree import ElementTree
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
import json


# curl -X GET http://127.0.0.1:8000/api/getWeatherData/Seoul/ -H "Authorization:Token *"


class getWeatherData(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    content = {}

    def get(self, request, city, format=None):
        now = datetime.now()

        content = getattr(self, "content")
        print(content)

        if content == {}:
            print("None, request Weather API")
            # content = {"weather":"Clear", "description":"clear sky", "name":city, "temp":"0.44", "humidity":"38", "pressure":"1029","dataTime":"2022-01-26T18:09:33.451768" }
            content = self.callOpenAPI(city)
            if content != {}:
                setattr(self, "content", content)
            return Response(content)

        elif now > (content["dataTime"] + relativedelta(minutes=30)):
            print("content updates before 3, request API for new")
            content = self.callOpenAPI(city)
            if content != {}:
                setattr(self, "content", content)
            return Response(content)

        else:
            print("now new content, don't update content dataTime")
            return Response(content)

    def callOpenAPI(self, city):
        now = datetime.now()
        accessApiTime = now

        servername = (
            "http://api.openweathermap.org/data/2.5/weather?q="
            + city
            + "&units=metric&appid="
            + WeatherApiKey
        )

        jsonString = requests.get(servername).text
        print(jsonString)

        # {"coord":{"lon":126.9778,"lat":37.5683},"weather":[{"id":800,"main":"Clear","description":"clear sky","icon":"01n"}],
        # "base":"stations","main":{"temp":-5.98,"feels_like":-8.65,"temp_min":-9.58,"temp_max":-3.31,"pressure":1028,"humidity":86},
        # "visibility":10000,"wind":{"speed":1.54,"deg":30},"clouds":{"all":0},"dt":1644337321,
        # "sys":{"type":1,"id":8105,"country":"KR","sunrise":1644359330,"sunset":1644397431},"timezone":32400,"id":1835848,"name":"Seoul","cod":200}

        jsonObject = json.loads(jsonString)
        jsonArray = jsonObject.get("weather")
        for dictweather in jsonArray:
            # {'id': 804, 'main': 'Clouds', 'description': 'overcast clouds', 'icon': '04n'}
            weather = dictweather.get("main")
            description = dictweather.get("description")

        temp = jsonObject.get("main").get("temp")
        feels_like = jsonObject.get("main").get("feels_like")
        pressure = jsonObject.get("main").get("pressure")
        humidity = jsonObject.get("main").get("humidity")

        wind_speed = jsonObject.get("wind").get("speed")
        wind_deg = jsonObject.get("wind").get("deg")

        content = {
            "weather": weather,
            "description": description,
            "temp": temp,
            "feels_like": feels_like,
            "pressure": pressure,
            "humidity": humidity,
            "wind_speed": wind_speed,
            "wind_deg": wind_deg,
            "dataTime": accessApiTime,
        }
        return content


# curl -X GET http://127.0.0.1:8000/api/getDustData/ -H "Authorization:Token *"


class getDustData(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    content = {}

    def get(self, request, format=None):
        now = datetime.now()

        content = getattr(self, "content")
        print(content)

        if content == {}:  # 1일 100번까지 호출 가능하므로 서버 실행 후 최초 실행되거나 30분이 안된 경우라면
            print("content None, request Dust API")
            content = self.callOpenAPI()
            if content != {}:
                setattr(self, "content", content)
            return Response(content)

        elif now > (content["dataTime"] + relativedelta(minutes=30)):
            print("content updates before 3, request Dust API for new")
            content = self.callOpenAPI()
            if content != {}:
                setattr(self, "content", content)
            return Response(content)

        else:
            print("now new dust content, don't update content dataTime")
            return Response(content)

            # {"pm25Value":36,"pm10Value":63,"o3Value":0.028,"pm25Grade":3,"pm10Grade":2,"o3Grade":1,"dataTime":"2022-01-26T18:09:33.451768"}

    def callOpenAPI(self):
        now = datetime.now()
        accessApiTime = now - timedelta(days=4)
        stationName = "종로"
        servername = (
            "http://apis.data.go.kr/B552584/ArpltnInforInqireSvc/getMsrstnAcctoRltmMesureDnsty?numOfRows=1&dataTerm=DAILY&ver=1.3&serviceKey="
            + KoreaApiKey2
            + "&stationName="
            + stationName
        )

        xmlString = requests.get(servername)
        # print(xmlString.text)

        accessApiTime = now

        start = xmlString.text.find("<body>")
        end = xmlString.text.find("<numOfRows>")

        body = xmlString.text[start + 6 : end]
        # print(body, file=sys.stdout)

        root_element = ElementTree.fromstring(body)

        items = []
        iter_element = root_element.iter(tag="item")
        for element in iter_element:
            result = {}
            result["o3Value"] = element.find("o3Value").text
            result["pm10Value"] = element.find("pm10Value").text
            result["pm25Value"] = element.find("pm25Value").text
            result["o3Grade"] = element.find("o3Grade").text
            result["pm10Grade"] = element.find("pm10Grade").text
            result["pm25Grade"] = element.find("pm25Grade").text
            items.append(result)

        pm25Value = int(items[0]["pm25Value"])
        pm10Value = int(items[0]["pm10Value"])
        o3Value = float(items[0]["o3Value"])
        pm25Grade = int(items[0]["pm25Grade"])
        pm10Grade = int(items[0]["pm10Grade"])
        o3Grade = int(items[0]["o3Grade"])

        if (int(items[0]["pm25Value"])) == 0:
            content = {}
            return content

        content = {
            "pm25Value": pm25Value,
            "pm10Value": pm10Value,
            "o3Value": o3Value,
            "pm25Grade": pm25Grade,
            "pm10Grade": pm10Grade,
            "o3Grade": o3Grade,
            "dataTime": accessApiTime,
        }
        return content

        # {"pm25Value":39,"dataTime":"2022-01-26T15:02:11.351947"}


""" 날짜 계산 
from datetime import datetime, timedelta
now = datetime.now()
print("현재 :" , now)			    # 현재 : 2021-01-09 19:41:03.645702
before_one_day = now - timedelta(days=1)
print("1일 전 :", before_one_day)	# 1일 전 : 2021-01-08 19:41:03.645702
result = now.strftime("%Y%m%d")
print(result)			            # 20220109
"""


class getCoronaData(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    content = {}

    # 매일 오전10시에 callOpenAPI() 자동 실행하도록

    def get(self, request, format=None):
        now = datetime.now()

        content = getattr(self, "content")
        print(content)

        if content == {}:  # 서버 실행 후 최초 실행되거나 30분이 안된 경우라면
            print("content None, request Corona API")
            content = self.callOpenAPI()
            if content != {}:
                setattr(self, "content", content)
            return Response(content)

        elif now > (content["dataTime"] + relativedelta(minutes=30)):
            print("content updates before 3, request Corona API for new")
            content = self.callOpenAPI()
            if content != {}:
                setattr(self, "content", content)
            return Response(content)

        else:
            print("now new Corona content, don't update content dataTime")
            return Response(content)

            # {"NewDecideCnt":13012,"NewAccExamCnt":84293,"NewDeathCnt":32,"dataTime":"2022-01-26T16:54:20.123305"}

    def callOpenAPI(self):
        now = datetime.now()
        before_four_day = now - timedelta(days=4)

        endCreateDt = now.strftime("%Y%m%d")
        startCreateDt = before_four_day.strftime("%Y%m%d")

        servername = (
            "http://openapi.data.go.kr/openapi/service/rest/Covid19/getCovid19InfStateJson?serviceKey="
            + CoronaApiKey
            + "&startCreateDt="
            + str(startCreateDt)
            + "&endCreateDt="
            + str(endCreateDt)
        )

        print(servername, file=sys.stdout)

        xmlString = requests.get(servername)
        # print(xmlString.text, file=sys.stdout)

        accessApiTime = now

        start = xmlString.text.find("<body>")
        end = xmlString.text.find("<numOfRows>")

        body = xmlString.text[start + 6 : end]
        # print(body, file=sys.stdout)

        root_element = ElementTree.fromstring(body)

        items = []
        iter_element = root_element.iter(tag="item")
        for element in iter_element:
            corona = {}
            corona["decideCnt"] = element.find("decideCnt").text
            corona["deathCnt"] = element.find("deathCnt").text
            items.append(corona)

        # print(items)
        # [{'decideCnt': '664391', 'accExamCnt': '20099870'}, {'decideCnt': '657505', 'accExamCnt': '19971712'}]
        # print(items[0]['accExamCnt'])   #20099870
        # print(items[1]['accExamCnt'])   #19971712

        decideCntValue = int(items[0]["decideCnt"]) - int(items[1]["decideCnt"])
        NewDeathCnt = int(items[0]["deathCnt"]) - int(items[1]["deathCnt"])

        if int(items[0]["decideCnt"]) == 0:
            content = {}
            return content

        # 신규 확진자, 검사자, 사망자 수, API 요청시간
        content = {
            "NewDecideCnt": decideCntValue,
            "NewAccExamCnt": 0,
            "NewDeathCnt": NewDeathCnt,
            "dataTime": accessApiTime,
        }
        return content


"""
from xml.etree import ElementTree
str_xml =   <animals>
                <animal><name>lion</name><lifespan>13</lifespan></animal>
                <animal><name>tiger</name><lifespan>17</lifespan></animal>
            </animals>

root_element = ElementTree.fromstring(str_xml)      # 문자열에서 XML을 파싱합니다
animals = []                                        # 동물리스트를 저장할 list 초기화한다
iter_element = root_element.iter(tag="animal")      # animal태그 iterator를 가져옵니다
for element in iter_element:                        # animal태그를 순회합니다
    animal = {}                                     # 각 동물을 저장할 dict 초기화한다
    animal['name'] = element.find("name").text      # name태그 값을 저장합니다
    animal['lifespan'] = element.find("lifespan").text  # lefespan태그 값을 저장합니다
    animals.append(animal)                          # 동물리스트에 동물정보를 저장합니다

print(animals)
#[{'name': 'lion', 'lifespan': '13'}, {'name': 'tiger', 'lifespan': '17'}]
"""


"""
#curl -X POST http://127.0.0.1:8000/api/iot/ojonghwa/ -d "item1=apple&item2=orenge"

@api_view(['GET', 'POST'])
def iot_esp8266(request, username):
    username = "Hi!, " + username
    
    if request.method == 'GET':
        username = username + " - GET Requested."
    elif request.method == 'POST':
        data1=request.data['item1']
        data2=request.data['item2']
        username = username + " - POST item1=" + data1 + ", item2=" + data2

    content = { 'orders': username }
    return Response(content, status=HTTP_200_OK)
"""

# curl -X POST http://127.0.0.1:8000/api/iot/ -H "Authorization:Token *" -d "espid=h01r01#001&temp=24.0&humi=53.5"


class iot_esp8266View(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, format=None):
        espid = request.data["espid"]
        temp = request.data["temp"]
        humi = request.data["humi"]

        post_request = "POST espid=" + espid + ", temp=" + temp + ", humi=" + humi
        print(post_request, file=sys.stdout)

        Esp8266.objects.create(espid=espid, temp=temp, humi=humi)

        content = {"request": "save ok"}
        return Response(content, status=HTTP_200_OK)


class OrderViewSet(viewsets.ReadOnlyModelViewSet):
    authentication_classes = [
        TokenAuthentication,
        BasicAuthentication,
        SessionAuthentication,
    ]
    permission_classes = [IsAdminUser]  # 관리자만 볼 수 있도록 제한
    queryset = Order.objects.all()
    serializer_class = OrderSerializer


class OrderItemDetailView(generics.RetrieveAPIView):
    authentication_classes = [
        TokenAuthentication,
        BasicAuthentication,
        SessionAuthentication,
    ]
    permission_classes = [IsAdminUser]
    queryset = OrderItem.objects.all()
    serializer_class = OrderItemSerializer


class OrderListDetailView(APIView):
    authentication_classes = [TokenAuthentication, BasicAuthentication]
    permission_classes = [IsAdminUser]

    def get(self, request, username, format=None):
        order_lists = (
            Order.objects.filter(user=username, paid=True).all().order_by("id")
        )
        order_items = OrderItem.objects.filter(order__in=order_lists)

        orderlist = []
        for order in order_lists:
            orderinfo = "order:"
            orderinfo = (
                orderinfo
                + str(order.id)
                + ","
                + str(order.get_total_cost())
                + ","
                + str(order.created)
            )
            orderlist.append(orderinfo)
            for item in order_items:
                if item.order.id == order.id:
                    tempstr = "item:{"
                    tempstr = (
                        tempstr
                        + str(item.product)
                        + ","
                        + str(item.price)
                        + ","
                        + str(item.quantity)
                        + "}"
                    )
                    orderlist.append(tempstr)

        content = {
            "orders": orderlist,
        }
        return Response(content)


# 527, Router viewsets
class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


# http://kbeautymania.com/api/product/?search=한글
# curl -X GET  http://kbeautymania.com/api/product/?search=php


class ProductViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Product.objects.all().order_by("id")
    serializer_class = ProductSerializer

    def get_queryset(self):
        qs = super().get_queryset()
        search = self.request.query_params.get("search", "")
        if search:
            qs = qs.filter(Q(name__icontains=search) | Q(slug__icontains=search))
        return qs


class CategoryProductViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategoryProductSerializer
    # pagination_class = LimitOffsetPagination


# http://kbeautymania.com/api/post/
# http://kbeautymania.com/api/post/?search=한글


class PostViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def get_queryset(self):
        qs = super().get_queryset()
        search = self.request.query_params.get("search", "")
        if search:
            qs = qs.filter(Q(body__icontains=search) | Q(title__icontains=search))
        return qs


class Login(APIView):
    def post(self, request):
        user = authenticate(
            username=request.data.get("username"), password=request.data.get("password")
        )
        if not user:
            return Response(
                {"error": "Credentials are incorrect or user does not exist"},
                status=HTTP_404_NOT_FOUND,
            )
        token, _ = Token.objects.get_or_create(user=user)
        return Response({"token": token.key}, status=HTTP_200_OK)


# curl -X GET http://kbeautymania.com/api/order/ -H "Authorization:Token ***"
# [{"id":1,"username":"admin","email":"ojonghwa@gmail.com"},{"id":2,"username":"ojonghwa","email":"ojonghwa@naver.com"},{"id":3,"username":"empas","email":"ojonghwa@empas.com"}]

# curl -X GET -u admin:ze http://kbeautymania.com/api/orderlist/


class Signup(CreateAPIView):
    model = User
    serializer_class = SignupSerializer
    permission_classes = [AllowAny]


# C:\>curl -X POST http://kbeautymania.com/api/login/ -d "username=testuser1&password=********"
# C:\>curl -X POST http://kbeautymania.com/api/signup/ -d "username=testuser1&password=********&email=test@naver.com"


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    # viewsets.ModelViewSet
    queryset = User.objects.all()
    serializer_class = UserSerializer
    authentication_classes = [
        TokenAuthentication,
        BasicAuthentication,
        SessionAuthentication,
    ]
    permission_classes = [IsAuthenticated]  # 회원 인증과 허가


"""
인증과 허가
개체 (정보/코드 등)에 대한 접근을 허용하기 위해서, 인증/식별만으로는 충분하지 않습니다. 추가로 각 개체에 대한 허가가 필요합니다.

DRF의 Permission System : 현재 요청에 대한 허용/거부를 결정, APIView 단위로 지정이 가능합니다.

AllowAny (디폴트 전역 설정) : 인증 여부에 상관없이 뷰 호출을 허용
IsAuthenticated : 인증된 요청에 한해서 뷰 호출 허용 (로그인이 되어있어야만 접근 허용)
IsAdminUser : Staff 인증 요청에 한해서 뷰 호출 허용
IsAuthenticatedOrReadOnly : 비인증 요청에게는 읽기 권한만 허용 (로그인이 되어 있지않아도 조회는 가능)
DjangoModelPermissons : 인증된 요청에 한하여 뷰 호출 허용, 추가로 장고 모델단위 Permissions 체크
DjangoModelPermissionsOrAnonReadOnly : DjangoModelPermissions와 유사, 비인증 요청에게는 읽기만 허용
DjangoObjectPermissons : 비인증 요청은 거부, 인증된 요청은 Object에 대한 권한 체크 수행
"""
