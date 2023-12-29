from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.response import Response
from django.core.exceptions import PermissionDenied

from products.models import Product, Category, Review
from .serializers import (ReviewSerializer,
                          ProductSerializer,
                          CategorySerializer)

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    def perform_update(self, serializer):
        super(CategoryViewSet, self).perform_update(serializer)

    def get_queryset(self):
        return Category.objects.all()

    def perform_destroy(self, instance):
        super(CategoryViewSet, self).perform_destroy(instance)

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def perform_create(self, serializer):
        serializer.save()

    def perform_update(self, serializer):
        product = get_object_or_404(Product, id=self.kwargs.get('pk'))
        
        new_quantity = serializer.validated_data.get('quantity')
        if new_quantity is not None and new_quantity < product.quantity:
            raise PermissionDenied('Изменение количества товара меньше текущего наличия!')

        super(ProductViewSet, self).perform_update(serializer)

    def perform_destroy(self, instance):
        if instance.quantity > 0:
            raise PermissionDenied('Нельзя удалить товар с ненулевым количеством!')

        super(ProductViewSet, self).perform_destroy(instance)

    def get_queryset(self):
        return Product.objects.all()

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)

        new_quantity = serializer.validated_data.get('quantity')
        if new_quantity is not None and new_quantity != instance.quantity:
            self.update_inventory(instance, new_quantity)

        self.perform_update(serializer)
        return Response(serializer.data)

class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer

    def get_queryset(self):
        products_pk = self.kwargs.get('products_pk')
        products = get_object_or_404(Product, id=products_pk)
        return products.reviews.all()

    def perform_create(self, serializer):
        product = get_object_or_404(Product, id=self.kwargs.get('products_pk'))
        serializer.save(author=self.request.user, product=product)

    def perform_update(self, serializer):
        review = get_object_or_404(Review, id=self.kwargs.get('pk'))
        if review.author != self.request.user:
            raise PermissionDenied('Изменение чужого контента запрещено!')
        super(ReviewViewSet, self).perform_update(serializer)