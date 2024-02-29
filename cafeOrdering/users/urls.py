from django.urls import path
from .views import sign_up, view_profile, report_problem

urlpatterns = [
    path('profile/', view_profile, name='view_profile'),
    path('sign_up/', sign_up, name='sign_up'),
    path('report_problem/', report_problem, name='report_problem'),
]