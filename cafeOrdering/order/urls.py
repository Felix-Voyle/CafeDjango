from django.urls import path
from . import views

urlpatterns = [
    path('', views.order, name='order'),
    path('search/', views.product_search, name='product_search'),
    path('<str:order_id>/edit/', views.edit_order, name='edit_order'),
    path('<int:order_id>/delete/', views.delete_order, name='delete_order'),
]