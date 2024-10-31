from django.db import models

class Item(models.Model):
    Item_name = models.CharField(max_length=100)
    Item_description = models.CharField(max_length=1000)
    Item_amount = models.IntegerField(default=1)
    