from django.contrib import admin


from .models import Favorite, ProductsNutriTypeA, PictureUser

# Register your models here.
@admin.register(Favorite)
class FavoriteManage(admin.ModelAdmin):
    pass


@admin.register(ProductsNutriTypeA)
class ProductManage(admin.ModelAdmin):
    pass


@admin.register(PictureUser)
class PictureManage(admin.ModelAdmin):
    pass

