
from rest_framework import serializers
from .models import *



class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'
        


class ProductSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(read_only=True)
    photoOne = serializers.ImageField(read_only=True)
    photoTwo = serializers.ImageField(read_only=True)
    photoThree = serializers.ImageField(read_only=True)
    photoFour = serializers.ImageField(read_only=True)  

    class Meta:
        model = Product
        fields = '__all__'

    def to_representation(self, instance):
        """Override to provide full URLs for image fields"""
        representation = super().to_representation(instance)
        request = self.context.get('request')

        for img_field in ['image', 'photoOne', 'photoTwo', 'photoThree', 'photoFour']:
            img = representation.get(img_field)
            if img and request is not None:
                # Build absolute URI for the image
                representation[img_field] = request.build_absolute_uri(img)
        return representation
    





class CartProductSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)

    class Meta:
        model = CartProduct
        fields = '__all__'


class CartSerializer(serializers.ModelSerializer):
    products = CartProductSerializer(source='cartproduct_set', many=True, read_only=True)
    # 'cartproduct_set' is the default reverse related name unless you set related_name in FK

    class Meta:
        model = Cart
        fields = ['id', 'total', 'created', 'account', 'products']



class OrderProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderProduct
        fields = '__all__'

class CheckoutSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderProduct
        fields = '__all__'
        exclude = ['cart', 'amount', 'orderstatus', 'ref', 'total', 'complete']

