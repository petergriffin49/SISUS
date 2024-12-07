from django.db import models
from django.contrib.auth.models import User

#
class Item(models.Model):
    Item_name = models.CharField(max_length=100)
    Item_description = models.CharField(max_length=1000)
    Item_amount = models.IntegerField(default=1)
    Item_lowStock = models.IntegerField(default=10)

    def __str__(self):
        return f"{self.Item_name} : {self.Item_description} ({self.Item_amount}/{self.Item_lowStock})"

#
class Item_User(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.username} - {self.item.Item_name}"

#
class Item_Edit(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    amount = models.IntegerField(default=1)
    time = models.DateField()
    
    def __str__(self):
        return f"{self.item.Item_name} @ {self.time}"


