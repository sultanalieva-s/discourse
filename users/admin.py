from django.contrib import admin

# Register your models here.
from users.models import *

admin.site.register(CustomUser)
admin.site.register(Organization)
admin.site.register(OrganizationType)
