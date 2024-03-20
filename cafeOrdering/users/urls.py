from django.urls import path
from .views import sign_up, my_orders, report_problem

urlpatterns = [
    path('profile/my_orders/', my_orders, name='my_orders'),
    path('sign_up/', sign_up, name='sign_up'),
    path('report_problem/', report_problem, name='report_problem'),
]