from django.db import models

# Create your models here.
class Mouse(models.Model):
    x_coord = models.IntegerField()
    y_coord = models.IntegerField()
    category = models.CharField(max_length=3, default="w")

    def __str__(self):
        return self.name
