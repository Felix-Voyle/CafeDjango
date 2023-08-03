from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib import admin
from django.contrib.sites.models import Site


# Unregister the Group model from the admin site
admin.site.unregister(Group)

# Unregister the Site model from the admin site
admin.site.unregister(Site)