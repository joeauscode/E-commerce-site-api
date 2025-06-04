from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, serializers
from django.shortcuts import get_object_or_404
from .serializers import *
from .models import *

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
        


from rest_framework.permissions import AllowAny
# product view
class ProductView(APIView):
    permission_classes = [AllowAny]  # allow public access

    def get(self, request):
        products = Product.objects.filter(is_active=True)
        serializer = ProductSerializer(products, many=True, context={'request': request})
        return Response(serializer.data)

# class ProductView(APIView):
#     def post(self, request):
#         try:
#             serializer = ProductSerializer(data=request.data)
#             if serializer.is_valid():
#                 serializer.save()
#                 return Response(serializer.data, status=status.HTTP_201_CREATED)
#             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#         except Exception as e:
#             return Response({"errors": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

#     def get(self, request):
#         try:
#             products = Product.objects.all()
#             serializer = ProductSerializer(products, many=True, context={'request': request})
#             return Response(serializer.data, status=status.HTTP_200_OK)
#         except Exception as e:
#             return Response({"errors": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# class ProductDetailsView(APIView):
#     def get(self, request, id):
#         try:
#             product = get_object_or_404(Product, id=id)
#             serializer = ProductSerializer(product, context={'request': request})
#             return Response(serializer.data, status=status.HTTP_200_OK)
#         except Exception as e:
#             return Response({"errors": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

#     def put(self, request, id):
#         try:
#             product = get_object_or_404(Product, id=id)
#             serializer = ProductSerializer(product, partial=True, data=request.data)
#             if serializer.is_valid():
#                 serializer.save()
#                 return Response(serializer.data, status=status.HTTP_200_OK)
#             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#         except Exception as e:
#             return Response({"errors": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

#     def delete(self, request, id):
#         try:
#             product = get_object_or_404(Product, id=id)
#             product.delete()
#             return Response({"message": "Product deleted"}, status=status.HTTP_200_OK)
#         except Exception as e:
#             return Response({"errors": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)





# add to cart

class AddToCartView(APIView):

    def post(self, request, id):
        try:

            product = get_object_or_404(product, id=id)
            pass
        except Exception as e:
            return Response({'errors':str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)