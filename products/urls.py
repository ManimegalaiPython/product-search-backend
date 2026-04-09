# products/urls.py
from django.urls import path
from django.http import JsonResponse
from . import views

def api_root(request):
    return JsonResponse({
        "message": "API is live",
        "endpoints": ["products/", "categories/", "brands/", "stats/"]
    })

urlpatterns = [
    path('', api_root),  # <-- fixes /api/ 404
    path('products/', views.ProductListView.as_view(), name='product-list'),
    path('products/<int:pk>/', views.product_detail, name='product-detail'),
    path('categories/', views.categories_view, name='categories'),
    path('brands/', views.brands_view, name='brands'),
    path('stats/', views.stats_view, name='stats'),
]
