from django.db.models import Count
from rest_framework.generics import ListAPIView, RetrieveAPIView, CreateAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated

from .serializers import CategoryListSerializer, ProductListSerializer, OrderValidator
from .models import Category, Product, Order


class CategoryListView(ListAPIView):
    permission_classes = (AllowAny,)
    serializer_class = CategoryListSerializer
    search_fields = ('name',)

    def get_queryset(self):
        return Category.objects.all().annotate(products_count=Count('products'))


class ProductListView(ListAPIView):
    permission_classes = (AllowAny,)
    serializer_class = ProductListSerializer
    search_fields = ('name', 'description')
    filterset_fields = ('category_id',)
    queryset = Product.objects.all()


class ProductDetailView(RetrieveAPIView):
    permission_classes = (AllowAny,)
    serializer_class = ProductListSerializer
    queryset = Product.objects.all()


class CreateOrderView(CreateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = OrderValidator
    queryset = Order.objects.all()
