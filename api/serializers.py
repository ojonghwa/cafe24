from rest_framework import serializers
from shop.models import Product, Category
from orders.models import Order, OrderItem
from blog.models import Post, Comment
from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email']


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']
        

class ProductSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    likers  = serializers.StringRelatedField(many=True)
    class Meta:
        model = Product
        fields = ['id', 'name', 'slug', 'price', 'category', 'image', 'publication_date',  
            'description', 'contributors', 'publisher', 'isbn', 'likers' ]


class CategoryProductSerializer(serializers.ModelSerializer):
    products = ProductSerializer(many=True, read_only=True)
    class Meta:
        model = Category
        fields = ['name', 'products']


class ItemtSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['name']


class OrderItemSerializer(serializers.ModelSerializer):
    product = ItemtSerializer()  
    class Meta:
        model = OrderItem
        fields = ['order', 'product', 'price', 'quantity']  

        
class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True)
    class Meta:
        model = Order
        #fields = ['fullname', 'mobile', 'created', 'get_total_cost', 'items']
        fields = '__all__'


class PostSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    product = ItemtSerializer(read_only=True)
    voter  = serializers.StringRelatedField(many=True)

    class Meta:
        model = Post
        fields = ['id','title','body','product','author','created','status','voter']
