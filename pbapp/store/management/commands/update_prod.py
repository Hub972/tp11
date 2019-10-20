from ...models import ProductsNutriTypeA
from ...request_.offs_req import AllRequests
from django.core.management.base import BaseCommand, CommandError
import json


class Command(BaseCommand):
    help = 'Update the openfoodfacts db '

    def handle(self, *args, **options):
        products = ProductsNutriTypeA.objects.all()
        req = AllRequests()
        c = 0
        for item in products:
            try:
                productr = req.code_request(item.code)
                productj = json.loads(productr.text)
                if 'product' in productj:
                    c += 1
                    print(c)
                    filtProduct = productj['product']

                product_name = filtProduct['product_name']
                picture = filtProduct['image_front_url']
                category = filtProduct['pnns_groups_2']
                if item.product_name != product_name:
                    print(item.code + ' ' + str(item.id))
                    change = ProductsNutriTypeA.objects.filter(code=item.code).order_by('id').first()
                    change.product_name = product_name
                    change.save()
                    print(f'{product_name} changé à la place de {item.product_name}')
                if item.picture != picture:
                    print(item.code+' '+str(item.id))
                    change = ProductsNutriTypeA.objects.filter(code=item.code).order_by('id').first()
                    change.picture = picture
                    change.save()
                    print(f'{picture} changé à la place de {item.picture}')
                if item.category != category:
                    print(item.code + ' ' + str(item.id))
                    change = ProductsNutriTypeA.objects.filter(code=item.code).order_by('id').first()
                    change.category = category
                    change.save()
                    print(f'{category} changé à la place de {item.category}')
            except KeyError:
                pass
