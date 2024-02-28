from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.sites.models import Site
from allauth.socialaccount.models import SocialAccount, SocialToken, SocialApp

from .models import UserProfile

class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'is_staff', 'is_workspace', 'address_line1', 'postcode']
    list_filter = ['is_staff', 'is_workspace']
    search_fields = ['user__username', 'address_line1', 'postcode']

admin.site.register(UserProfile, UserProfileAdmin)

# Unregister the Group model from the admin site
admin.site.unregister(Group)

# Unregister the Site model from the admin site
admin.site.unregister(Site)

admin.site.unregister({SocialAccount, SocialToken, SocialApp})