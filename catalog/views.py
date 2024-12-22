from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from users.models import CustomerDeliverWareHouse
from users.permission import IsBuyer, IsSellerOrAdmin
from warehouse.pagination import CustomPagination
from .models import Product, ProductStock
from .serializers import ProductSerializer, ProductFullSerializer
from django.db.models import F, Q


class CatalogView(APIView):
    permission_classes = (IsAuthenticated, IsBuyer)

    def get(self, request):
        city_id = request.user.city.id if request.user.city else None

        if not city_id:
            return Response({"detail": "У пользователя нет привязанного города"}, status=status.HTTP_400_BAD_REQUEST)

        ware_house_ids = CustomerDeliverWareHouse.objects.filter(user__id=request.user.id).values_list('warehouse_id', flat=True)
        if not ware_house_ids:
            return Response({"detail": "У пользователя нет склада"}, status=status.HTTP_404_NOT_FOUND)

        products = Product.objects.filter(product_stock__ware_house__id__in=ware_house_ids, product_stock__quantity__gt=0)
        paginator = CustomPagination()
        paginated_questions = paginator.paginate_queryset(products, request, view=self)
        serializer = ProductFullSerializer(paginated_questions, many=True,  context={'city_id': city_id})
        return paginator.get_paginated_response(serializer.data)

class ProductDetailView(APIView):
    permission_classes = (IsAuthenticated, IsBuyer)
    def get(self, request, product_id):
        try:
            product = Product.objects.get(id=product_id)
            product.views_count = F('views_count') + 1
            product.save()
            product.refresh_from_db()
            serializer = ProductFullSerializer(product)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Product.DoesNotExist:
            return Response({'detail': 'Продукт не найден'}, status=status.HTTP_404_NOT_FOUND)


class SearchView(APIView):
    permission_classes = (IsAuthenticated, IsBuyer)

    def get(self, request):
        query = self.request.query_params.get('q', '').strip()
        city_id = request.user.city.id if request.user.city else None

        if not city_id:
            return Response({"detail": "У пользователя нет привязанного города"}, status=status.HTTP_400_BAD_REQUEST)

        ware_house_ids = CustomerDeliverWareHouse.objects.filter(user_id=request.user.id).values_list('warehouse_id', flat=True)

        if not ware_house_ids:
            return Response({"detail": "У пользователя нет склада"}, status=status.HTTP_404_NOT_FOUND)

        products = Product.objects.filter(
            Q(name__icontains=query) | Q(product_description__description__icontains=query),
            product_stock__ware_house_id__in=ware_house_ids,
            product_stock__quantity__gt=0
        ).distinct()

        if not products.exists():
            return Response({"detail": "Ничего не найдено"}, status=status.HTTP_404_NOT_FOUND)

        serializer = ProductSerializer(products, many=True, context={'city_id': city_id})
        return Response(serializer.data, status=status.HTTP_200_OK)


from django.db import transaction
from itertools import islice

def chunked_iterable(iterable, chunk_size):
    """Yield successive chunks from iterable."""
    iterator = iter(iterable)
    while chunk := list(islice(iterator, chunk_size)):
        yield chunk

class UpdateStocksView(APIView):
    permission_classes = (IsAuthenticated, IsSellerOrAdmin)

    def post(self, request):
        data = request.data
        stocks_to_create = []
        stocks_to_update = []

        existing_stocks = ProductStock.objects.filter(
            product_id__in=[item['product_id'] for item in data],
            ware_house_id__in=[item['ware_house_id'] for item in data]
        ).values('id', 'product_id', 'ware_house_id')

        existing_stock_map = {(stock['product_id'], stock['ware_house_id']): stock['id'] for stock in existing_stocks}

        for stock_data in data:
            stock_id = existing_stock_map.get((stock_data['product_id'], stock_data['ware_house_id']))
            if stock_id:
                stocks_to_update.append(ProductStock(
                    id=stock_id,
                    quantity=stock_data['quantity'],
                    price=stock_data['price']
                ))
            else:
                stocks_to_create.append(ProductStock(
                    product_id=stock_data['product_id'],
                    ware_house_id=stock_data['ware_house_id'],
                    quantity=stock_data['quantity'],
                    price=stock_data['price']
                ))

        with transaction.atomic():
            for update_chunk in chunked_iterable(stocks_to_update, 200):
                ProductStock.objects.bulk_update(update_chunk, ['quantity', 'price'])

            for create_chunk in chunked_iterable(stocks_to_create, 200):
                ProductStock.objects.bulk_create(create_chunk)

        return Response({'detail': 'Данные о продукте успешно обновлены'}, status=status.HTTP_200_OK)