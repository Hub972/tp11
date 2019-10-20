from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Favorite(models.Model):
    name = models.CharField(max_length=200)
    generic_name = models.CharField(max_length=300)
    categorie = models.CharField(max_length=200)
    nutriscore = models.CharField(max_length=1)
    picture = models.CharField(max_length=600, null=True)
    id_user = models.ForeignKey(User, on_delete=models.CASCADE, default=00)


class ProductsNutriTypeA(models.Model):
    code = models.CharField(max_length=500, default="00")
    product_name = models.CharField(max_length=300, default="00")
    picture = models.CharField(max_length=500, default="00")
    category = models.CharField(max_length=200, default="00")


class PictureUser(models.Model):
    name = models.CharField(max_length=600, null=True)
    id_user = models.ForeignKey(User, on_delete=models.CASCADE)

