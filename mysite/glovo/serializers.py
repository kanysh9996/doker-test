from rest_framework import serializers
from .models import *
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ('username', 'email', 'password', 'first_name', 'last_name',
                  'age', 'phone_number', 'status', 'date_registered')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = UserProfile.objects.create_user(**validated_data)
        return user

    def to_representation(self, instance):
        refresh = RefreshToken.for_user(instance)
        return {
            'user': {
                'username': instance.username,
                'email': instance.email,
            },
            'access': str(refresh.access_token),
            'refresh': str(refresh),
        }


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        user = authenticate(**data)
        if user and user.is_active:
            return user
        raise serializers.ValidationError("Неверные учетные данные")



class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['first_name', 'last_name', 'status']


class UserSimpleProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['username']


class CategoryListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'category_name']


class CategorySimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['category_name']


class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = ['title', 'contact_number', 'social_network']


class ComboListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Combo
        fields = ['combo_name', 'combo_image', 'description', 'price']


class StoreCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Store
        fields = ['id', 'store_name', 'category', 'description', 'owner', 'address', 'store_image']


class StoreListSerializer(serializers.ModelSerializer):
    category = CategorySimpleSerializer(read_only=True)
    get_count_people = serializers.SerializerMethodField()
    get_good_stars = serializers.SerializerMethodField()

    class Meta:
        model = Store
        fields = ['id', 'store_name', 'store_image', 'category', 'get_count_people', 'get_good_stars']


    def get_count_people(self, obj):
        return obj.get_count_people


    def get_good_stars(self, obj):
        return obj.get_good_stars


class ComboDetailSerializer(serializers.ModelSerializer):
    store = StoreListSerializer()

    class Meta:
        model = Combo
        fields = ['combo_name', 'combo_image', 'description', 'price', 'store']

class ComboCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Combo
        fields = '__all__'


class CategoryDetailSerializer(serializers.ModelSerializer):
    category_store = StoreListSerializer(many=True, read_only=True)
    class Meta:
        model = Category
        fields = ['category_name', 'category_store']


class ProductListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['product_name', 'product_image', 'description', 'price']


class ProductDetailSerializer(serializers.ModelSerializer):
    store = StoreListSerializer()
    class Meta:
        model = Product
        fields = ['product_name', 'description', 'product_image', 'price', 'store']


class ProductCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'


class StoreReviewSerializer(serializers.ModelSerializer):
    client = UserSimpleProfileSerializer()
    created_date = serializers.DateTimeField(format('%d-%m-%Y %H:%M'))

    class Meta:
        model = StoreReview
        fields = ['client', 'text', 'stars', 'created_date']


class StoreCreateReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = StoreReview
        fields = '__all__'


class StoreDetailSerializer(serializers.ModelSerializer):
    contact = ContactSerializer(many=True, read_only=True)
    product_list = ProductListSerializer(many=True, read_only=True)
    combo_list = ComboListSerializer(many=True, read_only=True)
    owner = UserProfileSerializer()
    store_review = StoreReviewSerializer(many=True, read_only=True)
    category = CategorySimpleSerializer()


    class Meta:
        model = Store
        fields = ['store_name', 'store_image', 'description', 'address', 'category', 'owner', 'contact', 'product_list',
                  'combo_list', 'store_review']


class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = '__all__'


class CartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = '__all__'


class OrderCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'


class CourierSerializer(serializers.ModelSerializer):
    class Meta:
        model = Courier
        fields = '__all__'


class CourierCreateReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = CourierReview
        fields = '__all__'
