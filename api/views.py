from rest_framework import viewsets, generics
from rest_framework.views import APIView
from rest_framework.response import Response
#from rest_framework.pagination import LimitOffsetPagination

from rest_framework.authentication import BasicAuthentication, TokenAuthentication, SessionAuthentication
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from django.contrib.auth import authenticate
from rest_framework.status import HTTP_404_NOT_FOUND, HTTP_400_BAD_REQUEST, HTTP_200_OK, HTTP_201_CREATED
from rest_framework.authtoken.models import Token

from shop.models import Product, Category
from blog.models import Post, Comment
from orders.models import Order, OrderItem
from django.contrib.auth.models import User
from .serializers import ProductSerializer, CategorySerializer, CategoryProductSerializer, \
    OrderSerializer, OrderItemSerializer, PostSerializer, UserSerializer
from django.db.models import Q
import sys, requests
from cafe24.settings import KoreaApiKey2

#from rest_framework.decorators import api_view
from iot.models import Esp8266


#curl -X GET http://127.0.0.1:8000/api/getDustData/ -H "Authorization:Token f9ecad"

class getDustData(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):

        
        stationName  = "수지"
        #1일 100번까지 가능하므로 20분 간격으로 call 하도록 수정하고, 결과값을 변수에 담아두고 그 사이 호출 발생시 변수값을 반환 

        servername   = "http://apis.data.go.kr/B552584/ArpltnInforInqireSvc/getMsrstnAcctoRltmMesureDnsty?numOfRows=1&dataTerm=DAILY&ver=1.3&serviceKey=" + KoreaApiKey2 + "&stationName=" + stationName
  
        xmlString = requests.get(servername)
        #print(xmlString.text)

        start = xmlString.text.find("<pm25Value>")
        end   = xmlString.text.find("</pm25Value>")

        pm25Value = xmlString.text[start+11:end]
        pm25Value = int(pm25Value)

        content = { 'pm25Value': pm25Value }
        return Response(content)



'''
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
'''

#curl -X POST http://127.0.0.1:8000/api/iot/ -H "Authorization:Token f9ecad" -d "espid=h01r01#001&temp=24.0&humi=53.5"

class iot_esp8266View(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, format=None):
        espid=request.data['espid']
        temp=request.data['temp']
        humi=request.data['humi']

        post_request = "POST espid=" + espid + ", temp=" + temp + ", humi=" + humi
        print(post_request, file=sys.stdout)

        Esp8266.objects.create(espid=espid, temp=temp, humi=humi)

        content = { 'request': 'save ok' }
        return Response(content, status=HTTP_200_OK)



class OrderViewSet(viewsets.ReadOnlyModelViewSet):
    authentication_classes = [TokenAuthentication, BasicAuthentication, SessionAuthentication]
    permission_classes = [IsAdminUser]      #관리자만 볼 수 있도록 제한
    queryset = Order.objects.all()
    serializer_class = OrderSerializer



class OrderItemDetailView(generics.RetrieveAPIView):
    authentication_classes = [TokenAuthentication, BasicAuthentication, SessionAuthentication]
    permission_classes = [IsAdminUser]
    queryset = OrderItem.objects.all()
    serializer_class = OrderItemSerializer



class OrderListDetailView(APIView):
    authentication_classes = [TokenAuthentication, BasicAuthentication]
    permission_classes = [IsAdminUser]

    def get(self, request, username, format=None):
        order_lists = Order.objects.filter(user=username, paid=True).all().order_by('id')
        order_items = OrderItem.objects.filter(order__in=order_lists)
        
        orderlist=[]
        for order in order_lists:
            orderinfo = "order:"
            orderinfo = orderinfo + str(order.id) + ',' + str(order.get_total_cost()) + ',' + str(order.created)
            orderlist.append(orderinfo)
            for item in order_items:
                if item.order.id == order.id:
                    tempstr = "item:{"
                    tempstr = tempstr + str(item.product) + ',' + str(item.price) + ',' + str(item.quantity) + "}"
                    orderlist.append(tempstr)

        content = { 'orders': orderlist, }
        return Response(content)



#527, Router viewsets
class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


#http://khubeauty.shop/api/product/?search=한글
#curl -X GET  http://khubeauty.shop/api/product/?search=django

class ProductViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Product.objects.all().order_by('id')
    serializer_class = ProductSerializer

    def get_queryset(self):
        qs = super().get_queryset()
        search = self.request.query_params.get('search','')
        if search:
            qs = qs.filter(
                Q(name__icontains=search) | Q(slug__icontains=search)
            )
        return qs


class CategoryProductViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategoryProductSerializer
    #pagination_class = LimitOffsetPagination


#http://khubeauty.shop/api/post/
#http://khubeauty.shop/api/post/?search=한글

class PostViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def get_queryset(self):
        qs = super().get_queryset()
        search = self.request.query_params.get('search','')
        if search:
            qs = qs.filter(
                Q(body__icontains=search) | Q(title__icontains=search)
            )
        return qs



class Login(APIView):
    def post(self, request):
        user = authenticate(username=request.data.get("username"), password=request.data.get("password"))
        if not user:
            return Response({'error': 'Credentials are incorrect or user does not exist'}, status=HTTP_404_NOT_FOUND)
        token, _ = Token.objects.get_or_create(user=user)
        return Response({'token': token.key}, status=HTTP_200_OK)


#curl -X GET http://www.khubeauty.shop/api/order/ -H "Authorization:Token f9e94"
#[{"id":1,"username":"admin","email":"ojonghwa@gmail.com"},{"id":2,"username":"ojonghwa","email":"ojonghwa@naver.com"},{"id":3,"username":"empas","email":"ojonghwa@empas.com"}]

#curl -X GET -u admin:ze http://127.0.0.1:8000/api/orderlist/


class UserViewSet(viewsets.ReadOnlyModelViewSet):       
                  #viewsets.ModelViewSet
    queryset = User.objects.all()
    serializer_class = UserSerializer
    authentication_classes = [TokenAuthentication, BasicAuthentication, SessionAuthentication]
    permission_classes = [IsAuthenticated]     #회원 인증과 허가


'''
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
'''

