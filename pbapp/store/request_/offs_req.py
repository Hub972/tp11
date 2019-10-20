import requests


class AllRequests:

    def code_request(self, code):
        """request about code products"""
        req = requests.get(f"https://fr.openfoodfacts.org/api/v0/produit/{code}.json")
        return req

    def search_product_item(self, item):
        """request about item"""
        items = item.replace(' ', '%20')
        req = requests.get(
            f'https://fr.openfoodfacts.org/cgi/search.pl?search_terms={items}&search_simple=1&action=process&json=1')
        return req
