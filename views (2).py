from decimal import Decimal, InvalidOperation
from rest_framework import generics, permissions, filters
from .models import Category, Product
from .serializers import CategorySerializer, ProductSerializer

class CategoryListView(generics.ListAPIView):
    serializer_class = CategorySerializer
    permission_classes = [permissions.AllowAny]
    queryset = Category.objects.filter(is_active=True)

class ProductListView(generics.ListAPIView):
    serializer_class = ProductSerializer
    permission_classes = [permissions.AllowAny]
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ["price", "created_at", "name"]
    ordering = ["-created_at"]
    def get_queryset(self):
        qs = Product.objects.filter(status=Product.Status.ACTIVE, stock__gt=0).select_related("category", "seller")
        category = self.request.query_params.get("category")
        search = self.request.query_params.get("q")
        min_price = self.request.query_params.get("min_price")
        max_price = self.request.query_params.get("max_price")
        if category:
            qs = qs.filter(category__slug=category)
        if search:
            qs = qs.filter(name__icontains=search)
        try:
            if min_price is not None and Decimal(min_price) >= 0:
                qs = qs.filter(price__gte=Decimal(min_price))
            if max_price is not None and Decimal(max_price) >= 0:
                qs = qs.filter(price__lte=Decimal(max_price))
        except (InvalidOperation, ValueError):
            return qs.none()
        return qs
