from django.contrib import admin
from .models import Board

class BoardAdmin(admin.ModelAdmin):
    list_display = ('title',)
    pass

admin.site.register(Board, BoardAdmin)
