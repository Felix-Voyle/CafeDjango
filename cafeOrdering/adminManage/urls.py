from django.urls import path
from . import views

urlpatterns = [
    path('', views.manage, name='manage'),
    path('enquiries/', views.enquiries, name='enquiries'),
    path('create_invoice/', views.create_invoice, name='create_invoice'),
    path('update_order_status/', views.update_order_status, name='update_order_status'),
    path('<str:order_id>/invoice/', views.send_invoice, name='send_invoice')
]