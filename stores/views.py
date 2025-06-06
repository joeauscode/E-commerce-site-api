from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, serializers
from django.shortcuts import get_object_or_404
from .serializers import *
from .models import *
from django.db import transaction
from rest_framework.permissions import AllowAny




# from rest_framework.permissions import IsAuthenticated


# Create your views here.

# category view
class CategoryView(APIView):
    def post(self, request):
        try:
            serializers = CategorySerializer(data = request.data)
            if serializers.is_valid():
                serializers.save()
                return Response(serializers.data, status=status.HTTP_200_OK)
            return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"errors":str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    def get(self, request):
        try:
            category = Category.objects.all()
            serializers = CategorySerializer(category, many=True)
            return Response(serializers.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response ({'errors':str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# category get put and delete
class CategoryDetailsView(APIView):
    def get(self, request, id):
        try:
            category = get_object_or_404(Category, id=id)
            serializers = CategorySerializer(category)
            return Response (serializers.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'errors':str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    def put(self, request, id):
        try:
            category = get_object_or_404(Category, id=id)
            serializers = CategorySerializer(category, partial=True, data=request.data)
            if serializers.is_valid():
                serializers.save()
                return Response(serializers.data, status=status.HTTP_201_CREATED)
            return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error':str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
  
        
    def delete(self, requests, id):
        try:
            category = CategorySerializer(Category, id=id)
            category.delete()
            return Response({'message':'category deleted'}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error':str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        



# product view
class ProductView(APIView):
    permission_classes = [AllowAny]  # allow public access

    def get(self, request):
        products = Product.objects.filter(is_active=True)
        serializer = ProductSerializer(products, many=True, context={'request': request})
        return Response(serializer.data)
    
    




# add to cart






class AddToCartView(APIView):
    permission_classes = [AllowAny] 
    def post(self, request, id):
        try:
            product = get_object_or_404(Product, id=id)
            cart_id = request.session.get('cart_id', None)
            price = product.discount_Price if product.discount_Price else product.price

            with transaction.atomic():
                if cart_id:
                    cart = Cart.objects.filter(id=cart_id).first()
                    if cart is None:
                        cart = Cart.objects.create(total=0)
                        request.session['cart_id'] = cart.id

                    this_product_in_cart = CartProduct.objects.filter(cart=cart, product=product)

                    if this_product_in_cart.exists():
                        cartproduct = this_product_in_cart.first()
                        cartproduct.quantity += 1
                        cartproduct.total += price
                        cartproduct.save()

                        cart.total += price
                        cart.save()
                        return Response({'message': 'item increased in cart'})
                    else:
                        cartproduct = CartProduct.objects.create(
                            cart=cart, product=product, quantity=1, price=price, total=price
                        )
                        cart.total += price
                        cart.save()
                        return Response({'message': 'item added to cart'})
                else:
                    cart = Cart.objects.create(total=0)
                    request.session['cart_id'] = cart.id
                    cartproduct = CartProduct.objects.create(
                        cart=cart, product=product, quantity=1, price=price, total=price
                    )
                    cart.total += price
                    cart.save()
                    return Response({'message': 'new item added to cart'})
        except Exception as e:
            return Response({'errors': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        


   

class MyCartView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        try:
            cart_id = request.session.get('cart_id', None)
            if cart_id:
                cart = get_object_or_404(Cart, id=cart_id)
                serializer = CartSerializer(cart)  # pass instance, not class
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response({'message':'cart not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'errors': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)






# class UserCartAPIView(APIView):
#     permission_classes = [IsAuthenticated]

#     def get(self, request):
#         user = request.user
#         try:
#             cart = Cart.objects.get(account=user)
#         except Cart.DoesNotExist:
#             return Response({"detail": "No active cart found"}, status=404)

#         cart_products = CartProduct.objects.filter(cart=cart)
#         serializer = CartProductSerializer(cart_products, many=True, context={'request': request})

#         return Response({
#             "cart_id": cart.id,
#             "total": cart.total,
#             "products": serializer.data
#         })




