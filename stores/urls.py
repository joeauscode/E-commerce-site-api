from django.urls import path
from . import views


urlpatterns = [
    path('category/', views.CategoryView.as_view(), name="category"),
    path('category/<int:id>/', views.CategoryDetailsView.as_view(), name="category-details"),

    # product
    path('product/', views.ProductView.as_view(), name="product"),
    # path('product/<int:id>/', views.ProductDetailsView.as_view(), name="product-details"),
  
]