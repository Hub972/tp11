from django.http import request
from django.test import TestCase, RequestFactory
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from mock import patch
import json
from bs4 import BeautifulSoup


from .request_.offs_req import AllRequests
from .models import ProductsNutriTypeA, Favorite, PictureUser
from .views import my_count


# Create your tests here.
class IndexPageTestCase(TestCase):
    def test_index_page(self):
        """Test the main page """
        response = self.client.get(reverse('store:index'))
        self.assertEqual(response.status_code, 200)


class LoginTestDetailCase(TestCase):
    """Test login condition"""
    def setUp(self):
        self.contact = User.objects.create_user(username="marc", email="marc@mail.com", password='marc')
        self.pic = PictureUser.objects.create(name="marc", id_user=self.contact, picture="test.png")
        self.bad_user = 'jean_marc'

    def test_my_register_page(self):
        """Test register content, redirect and my place page """
        response = self.client.get(reverse('store:register'), follow=True)
        self.assertEqual(response.status_code, 200)
        soup = BeautifulSoup(response.content, features="html.parser")
        names = soup.find_all('input')
        self.assertEqual(names[2]['name'], 'name')
        self.assertEqual(names[3]['name'], 'email')
        self.assertEqual(names[4]['name'], 'passwd')
        self.assertEqual(names[5]['name'], 'picture')
        dataRegister = {
            'name': u'test',
            'email': u'test@mail.com',
            'passwd': u'test',
            'id_user': self.contact,
            'picture': u'test.png'
        }
        responsePost = self.client.post(reverse('store:register'), data=dataRegister)
        self.assertEqual(responsePost.status_code, 200)
        self.assertTemplateUsed(responsePost, 'store/thanks.html')
        userReg = authenticate(username='test', password='test')
        self.assertIsNotNone(userReg)
        foctory = RequestFactory()
        req = foctory.get('/my_count/')
        req.user = self.contact
        responseMyPlace = my_count(req)
        self.assertEqual(responseMyPlace.status_code, 200)

    def test_if_user_exist(self):
        """search user"""
        user = User.objects.get_by_natural_key("marc")
        self.assertEqual(user.email, self.contact.email)

    def test_if_user_dont_exist(self):
        """Verify bad user"""
        name = self.contact.username
        self.assertNotEqual(self.bad_user, name)

    def test_if_user_logout(self):
        """Test disconnect user"""
        response = self.client.get(reverse('store:logOut'))
        self.assertEqual(response.status_code, 302)

    def test_login_user(self):
        """Test reconnect user"""
        user = authenticate(username='marc', password='marc')
        self.assertTrue(user)

    def test_bad_login_user(self):
        """Test reconnect user"""
        user = authenticate(username='marc', password='m')
        self.assertFalse(user)


class MockCase(TestCase):
    """Test the search condition"""
    RESPONSE = {'status': 200, 'content': "CONTENT", 'json_data': None, 'raise_for_status': None}
    RESULT = json.dumps({"page_size": "20", "count": 204, "products": [
        {"nutrition_score_beverage": 0, "allergens": "NOISETTES, LAIT, LACTOSÉRUM, SOJA",
         "brands_tags": ["ferrero", "nutella"], "unique_scans_n": 727, "additives_n": 1, "product_name": "Nutella",
         "data_sources": "Database - FoodRepo / openfood.ch, Databases, Producer - Ferrero, Producers,"
                         " App - yuka, Apps",
         "no_nutrition_data": "", 'pnns_groups_2':'sweet', "selected_images": {"front": {
            "display": {"fr": "https://static.openfoodfacts.org/images/products/301/762/042/2003/front_fr.139.400.jpg"},
            "thumb": {"fr": "https://static.openfoodfacts.org/images/products/301/762/042/2003/front_fr.139.100.jpg"},
            "small": {
                "fr": "https://static.openfoodfacts.org/images/products/301/762/042/2003/front_fr.139.200.jpg"}}}}]})
    BADRESULT = json.dumps({"count": 0, "page_size": "20", "products": [], "skip": 0, "page": "1"})

    def setUp(self):
        self.code = [122334, 3175681854482]
        self.product_name = ['jus de pomme', 'confiture bio']
        self.picture = ['jus.png', 'confiture.png']
        self.category = ['beverage', 'sweet']
        for i, j in enumerate(self.code):
            u = ProductsNutriTypeA.objects.create(code=j, product_name=self.product_name[i], picture=self.picture[i],
                                                  category=self.category[i])
            u.save()
        self.productsBadItem = ProductsNutriTypeA.objects.filter(category="blal")
        self.productsGoodItem = ProductsNutriTypeA.objects.filter(category='sweet')[0]
        self.contact = User.objects.create_user(username="polo", email="polo@mail.com")
        self.prd = Favorite(
            name='confiture bio', generic_name='confiture bio', categorie='sweet', nutriscore='a',
            picture='confiture.png', id_user=self.contact)
        self.prd.save()

    @patch('store.request_.offs_req.AllRequests.search_product_item', return_value=RESULT)
    def test_offs_item_return(self, *args, **kwargs):
        """form's item"""
        req = AllRequests.search_product_item('Nutella')
        req = json.loads(req)
        self.assertEqual(req['count'], 204)
        self.assertEqual(req['products'][0]['pnns_groups_2'], 'sweet')

    @patch('store.views.search', return_value=RESPONSE)
    def test_view_search(self, *args, **kwargs):
        """We take the category of item search and return status 200"""
        self.assertEqual(self.productsGoodItem.product_name, 'confiture bio')
        self.assertEqual(self.productsGoodItem.picture, 'confiture.png')
        self.assertNotEqual(self.productsGoodItem.category, 'beverage')

    @patch('store.request_.offs_req.AllRequests.code_request', return_value=RESULT)
    def test_offs_code_return(self, *args, **kwargs):
        """Search by bar code"""
        req = AllRequests.code_request(112233445433)
        req = json.loads(req)
        self.assertEqual(req['page_size'], '20')

    def test_show_product(self):
        """Test show detail product"""
        response = self.client.get(reverse('store:detail', args=[self.productsGoodItem.id, ]))
        self.assertEqual(response.status_code, 200)

    @patch('store.request_.offs_req.AllRequests.search_product_item', return_value=BADRESULT)
    def test_offs_bad_item_return(self, *args, **kwargs):
        """Bad string"""
        req = AllRequests.search_product_item('hsfsgg')
        req = json.loads(req)
        self.assertEqual(req['count'], 0)


class AddAndReadProductToFavorite(TestCase):
    def setUp(self):
        self.contact = User.objects.create_user(username="polo", email="polo@mail.com")
        self.prd = Favorite(
            name='confiture bio', generic_name='confiture bio', categorie='sweet', nutriscore='a',
            picture='confiture.png', id_user=self.contact)
        self.prd.save()

    def test_show_product(self):
        """Test show product"""
        response = self.client.post(reverse('store:show',))
        self.assertEqual(response.status_code, 302)

    def test_product_in_db(self):
        """Test if product in Favorite"""
        product = Favorite.objects.get(id_user=self.prd.id_user)
        self.assertEquals(product.name, 'confiture bio')


class TermsPageTestCase(TestCase):
    """Test display terms"""
    def test_terms_page(self):
        response = self.client.get(reverse('store:terms'))
        self.assertEqual(response.status_code, 200)
