from django.urls import path
from . import views

urlpatterns = [

    # Catalog Views
    path('catalog/', views.CatalogView.as_view(), name='catalog'),
    path('product/<int:product_id>/', views.ProductDetailView.as_view(), name='product_detail'),
    path('search/', views.SearchView.as_view(), name='search'),

    # Update Stocks
    path('catalog/update/stocks/', views.UpdateStocksView.as_view(), name='update_stocks'),
]
