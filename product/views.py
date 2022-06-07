from django.http import Http404
from django.db.models import Q

from .serializers import ProductSerializer, CategorySerializer

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view

from .models import Product, Category


class LatestProductsList(APIView):
    def get(self, req, format=None):
        products = Product.objects.all()[0:4]
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)

class CategoryList(APIView):
    def get(self, req):
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data)

class ProductsFromCategory(APIView):
    def get_products(self, category_id):
        try:
            return Product.objects.filter(category=category_id)
        except Product.DoesNotExist:
            raise Http404
    
    def get(self, req, category_id):
        products = self.get_products(category_id)
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)
    
@api_view(['GET'])
def search(req):
    query = req.GET.get('query', '')

    if query:
        products = Product.objects.filter(Q(name__icontains=query) | Q(description__icontains=query))
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)
    else:
        return Response([])