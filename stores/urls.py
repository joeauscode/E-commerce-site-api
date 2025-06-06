from django.urls import path
from . import views


urlpatterns = [
    path('category/', views.CategoryView.as_view(), name="category"),
    path('category/<int:id>/', views.CategoryDetailsView.as_view(), name="category-details"),

    # product
    path('product/', views.ProductView.as_view(), name="product"),
    path('addtocart/<int:id>/', views.AddToCartView.as_view(), name='add-to-cart'),
    path('mycart/', views.MyCartView.as_view(), name='user-cart'),

  
]