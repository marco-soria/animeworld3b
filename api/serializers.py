from rest_framework import serializers

from django.contrib.auth.models import User

from .models import (
    Category,Product,
    Client,
    Order,OrderDetail,
    PaymentMethod,OrderPayment
)

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'
        
    def to_representation(self,instance):
        representation = super().to_representation(instance)
        return representation
        
class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'
        
    def to_representation(self,instance):
        representation = super().to_representation(instance)
        representation['image'] = instance.image.url
        return representation
    
class CategoryProductSerializer(serializers.ModelSerializer):
    products = ProductSerializer(many=True,read_only=True)
    
    class Meta:
        model = Category
        fields = ['id','name','products']
                
class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = '__all__'
        
    def to_representation(self,instance):
        representation = super().to_representation(instance)
        representation['fullname'] = instance.user.first_name + ' ' + instance.user.last_name
        representation['email'] = instance.user.email
        return representation
    
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username','first_name','last_name','email','password']
        extra_kwargs = {'password':{'write_only':True}}
        
    def create(self,validated_data):
        user = User(
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            username=validated_data['username']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user
    
class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id','username','first_name','last_name','email']
        
class UserFullSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username','first_name','last_name','email','password']
        extra_kwargs = {'password':{'write_only':True}}
        
class ClientFullSerializer(serializers.ModelSerializer):
    user = UserFullSerializer()
    
    class Meta:
        model = Client
        fields = ('user','phone','address')
        
    def create(self,validated_data):
        user_data = validated_data.pop('user')
        user = User.objects.create_user(**user_data)
        client = Client.objects.create(user=user,**validated_data)
        return client
    
class OrderDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderDetail
        fields = ('product','quantity','subtotal')
        
class OrderSerializer(serializers.ModelSerializer):
    details = OrderDetailSerializer(many=True)
    
    class Meta:
        model = Order
        fields = ['code','register_date','client','total_price','discount','details']
        
    def create(self,validated_data):
        list_details = validated_data.pop('details')
        order = Order.objects.create(**validated_data)
        for obj_detail in list_details:
            OrderDetail.objects.create(order=order,**obj_detail)
        return order
    
class PaymentMethodSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentMethod
        fields = '__all__'
        
    def to_representation(self,instance):
        representation = super().to_representation(instance)
        return representation
    
class OrderPaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderPayment
        fields = '__all__'
        
    def to_representation(self,instance):
        representation = super().to_representation(instance)
        representation['payment_method_name'] = instance.payment_method.name
        return representation
        
        