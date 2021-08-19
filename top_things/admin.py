from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Category, Thing


admin.site.register(User, UserAdmin)
admin.site.register(Category)
admin.site.register(Thing)

admin.site.site_title = "TopThings"
admin.site.site_header = "TopThings"






