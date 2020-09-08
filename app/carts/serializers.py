from action_serializer import ModelActionSerializer
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from carts.models import CartItem, Cart
from goods.serializers import MinimumGoodsSerializers, GoodsSaleSerializers


class CartItemSerializer(ModelActionSerializer):
    sub_total = serializers.SerializerMethodField()
    discount_payment = serializers.SerializerMethodField()
    goods = GoodsSaleSerializers(read_only=True)

    class Meta:
        model = CartItem
        fields = ('id', 'cart', 'goods', 'quantity', 'sub_total', 'discount_payment')
        action_fields = {
            'list': {
                'fields': ('id', 'goods', 'quantity', 'sub_total')
            },
            "update": {
                "fields": ('quantity',)
            },
        }

    def get_sub_total(self, obj):
        return obj.sub_total()

    def get_discount_payment(self, obj):
        return obj.discount_payment()


class CartItemCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = ('goods', 'quantity', 'cart')
        validators = [
            serializers.UniqueTogetherValidator(
                queryset=CartItem.objects.all(),
                fields=('goods', 'cart'),
                message=("already exists instanace.")
            )
        ]


class CartSerializer(ModelSerializer):
    item = CartItemSerializer(many=True)
    total_pay = serializers.SerializerMethodField()

    class Meta:
        model = Cart
        fields = ('id', 'item', 'total_pay')

    def get_total_pay(self, obj):
        return obj.total_pay
