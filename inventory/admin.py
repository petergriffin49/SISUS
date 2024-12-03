from django.contrib import admin

from .models import Item, Item_User, Item_Edit
admin.site.register(Item)
admin.site.register(Item_User)
admin.site.register(Item_Edit)

