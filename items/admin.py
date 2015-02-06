from django.contrib import admin
from .models import Item

class ItemAdmin(admin.ModelAdmin):
    list_display = ('title', 'modified', 'is_active')
    list_filter = ['is_active', 'modified']
    search_fields = ['title', 'description']


admin.site.register(Item, ItemAdmin)
