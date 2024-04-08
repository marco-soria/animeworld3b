from rest_framework import generics
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404

from .models import (
    Category,Product,
    Client,Order,
    PaymentMethod,
    OrderPayment, Favorite
)

from .serializers import (
    CategorySerializer,
    ProductSerializer,
    CategoryProductSerializer,
    ClientSerializer,
    UserSerializer,
    UserUpdateSerializer,
    ClientFullSerializer,
    OrderSerializer,
    PaymentMethodSerializer,
    OrderPaymentSerializer,
    FavoriteSerializer
)

from django.contrib.auth.models import User

class CategoryView(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    
class ProductView(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

class CategoryProductsView(generics.RetrieveAPIView):
    queryset = Category.objects.all()
    lookup_url_kwarg = 'category_id'
    serializer_class = CategoryProductSerializer
    
class ClientView(generics.ListCreateAPIView):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer
    
class ClienteDetailView(generics.RetrieveUpdateAPIView):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer
    
class ClienteDetailByUserView(generics.RetrieveAPIView):
    serializer_class = ClientSerializer
    
    def get_object(self):
        user_id = self.kwargs.get('user_id')
        user = User.objects.get(pk=user_id)
        
        client = Client.objects.filter(user=user).first()
        
        return client
    
class UserView(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    
class UserDetailView(generics.RetrieveUpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserUpdateSerializer
    
class ClientFullView(generics.ListCreateAPIView):
    queryset = Client.objects.all()
    serializer_class = ClientFullSerializer
    
class OrderView(generics.ListCreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    
class PaymentMethodView(generics.ListCreateAPIView):
    queryset = PaymentMethod.objects.all()
    serializer_class = PaymentMethodSerializer
    
class OrderPaymentView(generics.ListCreateAPIView):
    queryset = OrderPayment.objects.all()
    serializer_class = OrderPaymentSerializer
    

#view category product
class CategoryProductListView(generics.ListAPIView):
    serializer_class = CategoryProductSerializer

    def get_queryset(self):
        category_name = self.kwargs['category_name']
        try:
            category = Category.objects.get(name=category_name)
            return [category]
        except Category.DoesNotExist:
            return []
        
class FavoriteListView(generics.ListCreateAPIView):
    queryset = Favorite.objects.all()
    serializer_class = FavoriteSerializer

class FavoriteDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Favorite.objects.all()
    serializer_class = FavoriteSerializer


from rest_framework.authtoken.models import Token

class ToggleFavoriteView(APIView):
    def post(self, request, pk):
        # Verificar si el usuario está autenticado
        if request.user.is_authenticated:
            # Obtener el cliente asociado al usuario autenticado
            client = Client.objects.get(user=request.user)
            product = Product.objects.get(id=pk)
            favorite = Favorite.objects.filter(client=client, product=product).first()
            if favorite:
                favorite.delete()
                data = {'message': 'Producto eliminado de favoritos'}
            else:
                favorite = Favorite(client=client, product=product)
                favorite.save()
                data = {'message': 'Producto agregado a favoritos'}
            return Response(data)
        else:
            # Si el usuario no está autenticado, devolver un error de autorización
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        
class AuthenticatedProductView(generics.ListAPIView):
    queryset = Product.objects.all()

    def get_serializer_context(self):
        context = super().get_serializer_context()  # Get the existing context
        context['request'] = self.request  # Add the request to the context
        return context

    def get_serializer_class(self):
        return ProductSerializer