from django.contrib import admin
from .models import Fcuser

class FcuserAdmin(admin.ModelAdmin):
    pass

admin.site.register(Fcuser, FcuserAdmin)