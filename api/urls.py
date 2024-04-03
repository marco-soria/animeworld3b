from django.urls import path

from . import views

urlpatterns = [
    path('categories', views.CategoryView.as_view()),
    path('products',views.ProductView.as_view()),
    path('category/<int:category_id>/products',views.CategoryProductsView.as_view()),
    path('client',views.ClientView.as_view()),
    path('user',views.UserView.as_view()),
    path('user/<int:pk>',views.UserDetailView.as_view()),
    path('client/<int:pk>',views.ClienteDetailView.as_view()),
    path('client/full',views.ClientFullView.as_view()),
    path('client/byuser/<int:user_id>',views.ClienteDetailByUserView.as_view()),
    path('order',views.OrderView.as_view()),
    path('paymentmethod',views.PaymentMethodView.as_view()),
    path('order/payment',views.OrderPaymentView.as_view())
]