"""
URL configuration for cafeOrdering project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from users.views import sign_up, my_orders, redirect_from_profile
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('', include('homepage.urls')),
    path('accounts/signup/', sign_up, name='account_signup'),
    path('accounts/profile/', redirect_from_profile, name='redirect_from_profile'),
    path('accounts/', include('users.urls')),
    path('accounts/', include('allauth.urls')),
    path('admin/', admin.site.urls),
    path('enquire/', include('enquire.urls')),
    path('manage/', include('adminManage.urls')),
    path('order/', include('order.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
