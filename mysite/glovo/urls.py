from django.urls import path, include
from rest_framework import routers

from .views import (UserProfileViewSet, CartViewSet, CartItemViewSet, OrderCreateAPIView, CourierViewSet, StoreCreateReviewAPIView,
StoreListAPIView, StoreDetailAPIView, StoreCreateAPIView, CategoryListAPIView, CategoryDetailAPIView, ProductListAPIView,
ProductDetailAPIView, ProductCreateAPIView, ComboDetailAPIView, ComboListAPIView, ComboCreateAPIView, CourierCreateReviewAPIView,
RegisterView, LogoutView, CustomLoginView
)


router = routers.SimpleRouter()
router.register(r'user/', UserProfileViewSet, basename='user_list')
router.register(r'cart/', CartViewSet, basename='cart_list')
router.register(r'cart_item/', CartItemViewSet, basename='cart_item_list')
router.register(r'courier/', CourierViewSet, basename='courier_list')



urlpatterns = [
    path('', include(router.urls)),
    path('store/', StoreListAPIView.as_view(), name='store_list'),
    path('store/<int:pk>', StoreDetailAPIView.as_view(), name='store_detail'),
    path('store_create/', StoreCreateAPIView.as_view(), name='store_create'),
    path('category/', CategoryListAPIView.as_view(), name='category_list'),
    path('category/<int:pk>/', CategoryDetailAPIView.as_view(), name='category_detail'),
    path('product/create/', ProductCreateAPIView.as_view(), name='product_create'),
    path('product/', ProductListAPIView.as_view(), name='product_list'),
    path('product/<int:pk>/', ProductDetailAPIView.as_view(), name='product_detail'),
    path('store/review/', StoreCreateReviewAPIView.as_view(), name='store_review'),
    path('courier/review/', CourierCreateReviewAPIView.as_view(), name='courier_review'),
    path('combo/create/', ComboCreateAPIView.as_view(), name='combo_create'),
    path('combo/', ComboListAPIView.as_view(), name='combo_list'),
    path('combo/<int:pk>/', ComboDetailAPIView.as_view(), name='combo_detail'),
    path('order/create/', OrderCreateAPIView.as_view(), name='order_create'),
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout')
]