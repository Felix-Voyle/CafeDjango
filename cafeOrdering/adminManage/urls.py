from django.urls import path
from . import views

urlpatterns = [
    path('', views.manage, name='manage'),
    path('filter_orders/', views.filter_orders, name='filter_orders'),
    path('enquiries/', views.enquiries, name='enquiries'),
    path('manage_invoices/', views.manage_invoices, name='manage_invoices'),
    path('manage_invoices/<str:invoice_reference>/invoice_paid/', views.mark_invoice_paid, name="mark_invoice_paid"),
    path('filter_invoices/', views.filter_invoices, name='filter_invoices'),
    path('enquiry/<int:enquiry_id>/', views.enquiry, name='enquiry'),
    path('enquiry/delete/<int:enquiry_id>/', views.delete_enquiry, name='delete_enquiry'),
    path('create_invoice/', views.create_invoice, name='create_invoice'),
    path('send_created_invoice/', views.send_created_invoice, name='send_created_invoice'),
    path('update_order_status/', views.update_order_status, name='update_order_status'),
    path('<str:order_id>/add_services/', views.add_services, name='add_services'),
    path('<str:order_id>/send_invoice/', views.send_invoice, name='send_invoice'),
    path('<str:invoice_reference>/download_invoice', views.download_invoice, name='download_invoice'),
]