from django.db import models

class Item(models.Model):
    name = models.CharField(max_length=255)
    image = models.ImageField(upload_to='item_images/')
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=0)
    stock = models.PositiveIntegerField(default=0)
    # category = models.ForeignKey('Category', on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.name

