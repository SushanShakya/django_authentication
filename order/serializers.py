from rest_framework.serializers import ModelSerializer
from .models import Order, OrderItem
from product.serializers import ProductSerializer

class OrderItemSerializer(ModelSerializer):
    product = ProductSerializer
    class Meta:
        model = OrderItem
        fields = (
            "product",
            "quantity",
            "price"
        )

class OrderSerializer(ModelSerializer):
    items = OrderItemSerializer(many=True)
    class Meta:
        model = Order
        fields = (
            'id',
            'phone',
            'address',
            'created',
            'paid_amount',
            'items'
        )
    
    def create(self, validated_data):
        items_data = validate_data.pop('items')
        order = Order.objects.create(**validate_data)

        for item_data in items_data:
            OrderItem.objects.create(order=order, **item_data)
        
        return order

