from django.contrib import admin
from django.contrib.admin.apps import AdminConfig

from fly_admin.admin_settings import AdminSiteSettingsMixin
from fly_admin.admin_views import AdminViewsMixin


class FlyAdminSite(AdminSiteSettingsMixin, AdminViewsMixin):
   pass 


class FlyAdminConfig(AdminConfig):
    # https://docs.djangoproject.com/en/4.2/ref/contrib/admin/#customizing-the-adminsite-class

    default_site = "fly_admin.admin.FlyAdminSite"
