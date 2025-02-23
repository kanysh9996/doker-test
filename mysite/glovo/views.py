from django.shortcuts import render
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, generics, status
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView
from .models import (UserProfile, Category, Store, Product, Cart, CartItem,
     Order, Courier, StoreReview, Combo
)
from .serializers import (UserProfileSerializer, CategoryListSerializer, CategoryDetailSerializer , StoreListSerializer,
    StoreDetailSerializer, ProductListSerializer, CartSerializer,CartItemSerializer,
    CourierCreateReviewSerializer,OrderCreateSerializer, CourierSerializer, StoreCreateSerializer, ProductCreateSerializer,
    ProductDetailSerializer, StoreCreateReviewSerializer, ComboListSerializer, ComboDetailSerializer, ComboCreateSerializer,
    LoginSerializer, UserSerializer
)
from .permissions import CheckUser, CheckStatus, CheckStoreOwner
from .paginations import StorePagination, CategoryPagination, ProductPagination


class RegisterView(generics.CreateAPIView):
    serializer_class = UserSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class CustomLoginView(TokenObtainPairView):
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
        except Exception:
            return Response({"detail": "Неверные учетные данные"}, status=status.HTTP_401_UNAUTHORIZED)

        user = serializer.validated_data
        return Response(serializer.data, status=status.HTTP_200_OK)


class LogoutView(generics.GenericAPIView):
    def post(self, request, *args, **kwargs):
        try:
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception:
            return Response(status=status.HTTP_400_BAD_REQUEST)



class UserProfileViewSet(viewsets.ModelViewSet):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer

    def get_queryset(self):
        return UserProfile.objects.filter(id=self.request.user.id)


class CategoryListAPIView(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategoryListSerializer
    pagination_class = CategoryPagination


class CategoryDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategoryDetailSerializer


class StoreCreateAPIView(generics.CreateAPIView):
    queryset = Store.objects.all()
    serializer_class = StoreCreateSerializer
    permission_classes = [CheckUser]


class StoreListAPIView(generics.ListAPIView):
    queryset = Store.objects.all()
    serializer_class = StoreListSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['store_name']
    search_fields = ['category']
    ordering_fields = ['owner']
    pagination_class = StorePagination


class StoreDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Store.objects.all()
    serializer_class = StoreDetailSerializer
    permission_classes = [CheckUser, CheckStoreOwner]


class ProductListAPIView(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductListSerializer
    pagination_class = ProductPagination


class ProductDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductDetailSerializer


class ProductCreateAPIView(generics.CreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductCreateSerializer


class ComboListAPIView(generics.ListAPIView):
    queryset = Combo.objects.all()
    serializer_class = ComboListSerializer


class ComboDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Combo.objects.all()
    serializer_class = ComboDetailSerializer


class ComboCreateAPIView(generics.CreateAPIView):
    queryset = Combo.objects.all()
    serializer_class = ComboCreateSerializer


class CartViewSet(viewsets.ModelViewSet):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer


class CartItemViewSet(viewsets.ModelViewSet):
    queryset = CartItem.objects.all()
    serializer_class = CartItemSerializer


class OrderCreateAPIView(generics.CreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderCreateSerializer


class CourierViewSet(viewsets.ModelViewSet):
    queryset = Courier.objects.all()
    serializer_class = CourierSerializer


class StoreCreateReviewAPIView(generics.CreateAPIView):
    queryset = StoreReview.objects.all()
    serializer_class = StoreCreateReviewSerializer
    permission_classes = [CheckStatus]


class CourierCreateReviewAPIView(generics.CreateAPIView):
    queryset = Courier.objects.all()
    serializer_class = CourierCreateReviewSerializer