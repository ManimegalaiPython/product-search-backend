from django.urls import path
from . import views

urlpatterns = [
    path('products/',          views.ProductListView.as_view(), name='product-list'),
    path('products/<int:pk>/', views.product_detail,            name='product-detail'),
    path('categories/',        views.categories_view,           name='categories'),
    path('brands/',            views.brands_view,               name='brands'),
    path('stats/',             views.stats_view,                name='stats'),
]
