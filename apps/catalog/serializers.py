from django.db import transaction
from rest_framework import serializers

from .models import Category, Product, Order, OrderItem


class ProductListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'name', 'price', 'image', 'description', 'category']


class CategoryListSerializer(serializers.ModelSerializer):
    products_count = serializers.IntegerField()

    class Meta:
        model = Category
        fields = ['id', 'name', 'products_count']


class OrderItemValidator(serializers.Serializer):
    product = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all())
    quantity = serializers.IntegerField()


class OrderValidator(serializers.ModelSerializer):
    products = OrderItemValidator(many=True, write_only=True)

    def create(self, validated_data):
        order_items = []
        user = self.context.get('request').user
        email = user.email if user.is_authenticated else validated_data.get('email')

        with transaction.atomic():
            order = Order.objects.create(
                user=user if user.is_authenticated else None,
                address=validated_data.get('address'),
                email=email
            )

            for i in validated_data.get('products'):
                product = i.get('product')
                order_item = OrderItem(
                    price=product.price,
                    amount=product.price * i.get('quantity'),
                    order=order,
                    **i
                )
                order_items.append(order_item)

            OrderItem.objects.bulk_create(order_items)

        return order

    class Meta:
        model = Order
        fields = ['email', 'address', 'products']
        extra_kwargs = {'email': {'allow_blank': True}}
