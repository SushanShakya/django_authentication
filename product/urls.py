from django.urls import path, include

from . import views

urlpatterns = [
    path('latest', views.LatestProductsList.as_view()),
    path('categories', views.CategoryList.as_view()),
    path('products/<int:category_id>', views.ProductsFromCategory.as_view()),
    path('products/search', views.search)
] 