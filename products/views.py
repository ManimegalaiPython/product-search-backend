"""
Product Search API — views.py
Endpoint: GET /api/products/
Params:   search=, category=, brand=, min_price=, max_price=,
          min_rating=, in_stock=, sort_by=, page=
"""
from django.db.models import Q
from rest_framework import generics
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.exceptions import NotFound
from .models import Product, Category
from .serializers import ProductSerializer, CategorySerializer


class ProductListView(generics.ListAPIView):
    """
    GET /api/products/
    Works with both ?search= (your original param) and ?q= (common convention).
    """
    serializer_class = ProductSerializer

    def get_queryset(self):
        qs = Product.objects.select_related('category').all()

        # Accept both ?search= and ?q= for compatibility
        search = (
            self.request.query_params.get('search', '') or
            self.request.query_params.get('q', '')
        ).strip()

        if search:
            qs = qs.filter(
                Q(name__icontains=search)        |
                Q(description__icontains=search) |
                Q(brand__icontains=search)       |
                Q(category__name__icontains=search)
            )

        category = self.request.query_params.get('category', '').strip()
        if category:
            # Works with both slug (electronics) and name (Electronics)
            qs = qs.filter(
                Q(category__slug__iexact=category) |
                Q(category__name__iexact=category)
            )

        brand = self.request.query_params.get('brand', '').strip()
        if brand:
            qs = qs.filter(brand__iexact=brand)

        try:
            min_price = self.request.query_params.get('min_price')
            if min_price:
                qs = qs.filter(price__gte=float(min_price))
        except ValueError:
            pass

        try:
            max_price = self.request.query_params.get('max_price')
            if max_price:
                qs = qs.filter(price__lte=float(max_price))
        except ValueError:
            pass

        try:
            min_rating = self.request.query_params.get('min_rating')
            if min_rating:
                qs = qs.filter(rating__gte=float(min_rating))
        except ValueError:
            pass

        in_stock = self.request.query_params.get('in_stock', '').lower()
        if in_stock == 'true':
            qs = qs.filter(stock__gt=0)

        sort_map = {
            'price_asc':  'price',
            'price_desc': '-price',
            'rating':     '-rating',
            'name':       'name',
            'newest':     '-created_at',
        }
        sort_by = self.request.query_params.get('sort_by', 'newest')
        qs = qs.order_by(sort_map.get(sort_by, '-created_at'))

        return qs


@api_view(['GET'])
def product_detail(request, pk):
    """GET /api/products/<id>/"""
    try:
        product = Product.objects.select_related('category').get(pk=pk)
    except Product.DoesNotExist:
        raise NotFound(detail=f'Product {pk} not found.')
    return Response(ProductSerializer(product, context={'request': request}).data)


@api_view(['GET'])
def categories_view(request):
    """GET /api/categories/"""
    cats = Category.objects.all()
    return Response(CategorySerializer(cats, many=True).data)


@api_view(['GET'])
def brands_view(request):
    """GET /api/brands/"""
    brands = Product.objects.values_list('brand', flat=True).distinct().order_by('brand')
    return Response(list(brands))


@api_view(['GET'])
def stats_view(request):
    """GET /api/stats/"""
    return Response({
        'total_products':   Product.objects.count(),
        'total_categories': Category.objects.count(),
        'in_stock':         Product.objects.filter(stock__gt=0).count(),
        'featured':         Product.objects.filter(is_featured=True).count(),
    })
