from django.urls import path
from . import views

urlpatterns = [
    path('', views.manage, name='manage'),
    path('update_order_status/', views.update_order_status, name='update_order_status'),
]