from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.sites.models import Site
from allauth.socialaccount.models import SocialAccount, SocialToken, SocialApp


# Unregister the Group model from the admin site
admin.site.unregister(Group)

# Unregister the Site model from the admin site
admin.site.unregister(Site)

admin.site.unregister({SocialAccount, SocialToken, SocialApp})