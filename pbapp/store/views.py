from django.shortcuts import render, get_object_or_404, get_list_or_404, render_to_response
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.contrib.auth import authenticate, login, logout
import random
import logging

from .forms import Register, ParagraphErrorList, SearchProduct, LogIn, ChangePassword
from .request_.offs_req import AllRequests
from .models import ProductsNutriTypeA, Favorite, PictureUser


logger = logging.getLogger(__name__)

# Create your views here.


def index(request):
    """Display index page"""
    user = request.user.id
    if user:
        form = SearchProduct()
        context = {
            'form': form,
            'user': True
        }
        return render(request, 'store/index.html', context)
    else:
        form = SearchProduct()
        context = {'form': form, 'user': False}
        return render(request, 'store/index.html', context)


def register_(request):
    """display register page"""
    form = SearchProduct()
    if request.method == 'POST':
        formr = Register(request.POST, error_class=ParagraphErrorList)
        if formr.is_valid():
            name = formr.cleaned_data['name']
            emailUser = formr.cleaned_data['email']
            passwd = formr.cleaned_data['passwd']
            user = User.objects.create_user(username=name, email=emailUser, password=passwd)
            user.save()
            formlg = LogIn()
            context = {
                'form': form}
            return render(request, 'store/thanks.html', context)
        else:
            forml = Register()
            context = {
                'logEr': True,
                'forml': forml,
                'form': form,
            }
            return render(request, 'store/register_user.html', context)
    else:
        forml = Register()
        context = {
            'forml': forml,
            'form': form,
        }
        return render(request, 'store/register_user.html', context)


def login_(request):
    """log form"""
    form = SearchProduct()
    formlg = LogIn()
    context = {'formlg': formlg,
               'form': form}
    return render(request, 'store/login.html', context)


def my_count(request):
    """account page"""
    form = SearchProduct()
    passForm = ChangePassword()
    user = request.user.id
    try:
        picture = PictureUser.objects.get(id_user=user)
        picture = picture.name
    except Exception:
        picture = ";-)"

    detUser = get_object_or_404(User, pk=user)
    name = detUser.username
    mail = detUser.email
    context = {'name': name,
               'mail': mail,
               'form': form,
               'picture': picture,
               'passwd': passForm,
               }
    return render(request, 'store/my_place.html', context)


def change_password(request):
    """Script for confirm and change password user"""
    if request.method == 'POST':
        formp = ChangePassword(request.POST, error_class=ParagraphErrorList)
        if formp.is_valid():
            userId = request.user.id
            detUser = get_object_or_404(User, pk=userId)
            passwd = formp.cleaned_data['passwd']
            confPasswd = formp.cleaned_data['confPasswd']
            if passwd != confPasswd:
                form = SearchProduct()
                passForm = ChangePassword()
                try:
                    picture = PictureUser.objects.get(id_user=userId)
                    picture = picture.name
                except Exception:
                    picture = ";-)"
                context = {
                    'name': detUser.username,
                    'mail': detUser.email,
                    'form': form,
                    'picture': picture,
                    'passwd': passForm,
                    'logEr': True
                }
                return render(request, 'store/my_place.html', context)
            else:
                detUser.set_password(passwd)
                detUser.save()
                form = SearchProduct()
                passForm = ChangePassword()
                try:
                    picture = PictureUser.objects.get(id_user=userId)
                    picture = picture.name
                except Exception:
                    picture = ";-)"
                context = {
                    'name': detUser.username,
                    'mail': detUser.email,
                    'form': form,
                    'picture': picture,
                    'passwd': passForm,
                    'done': True
                }
                return render(request, 'store/my_place.html', context)


def connect_user(request):
    """Connect the users"""
    if request.method == 'POST':
        form = LogIn(request.POST, error_class=ParagraphErrorList)
        if form.is_valid():
            name = form.cleaned_data['name']
            passwd = form.cleaned_data['passwd']
            user = authenticate(username=name, password=passwd)
            if user is None:
                forml = Register()
                formlg = LogIn()
                form = SearchProduct()
                context = {
                    'user': False,
                    'logEr': True,
                    'forml': forml,
                    'formlg': formlg,
                    'form': form
                }
                return render(request, 'store/login.html', context)
            else:
                login(request, user)
                form = SearchProduct()
                context = {
                    "welcome": True,
                    "form": form
                }
                return render(request, 'store/index.html', context)


def search(request):
    """Display the results for the request"""
    user = request.user.id
    if user:
        user = True
    else:
        user = False
    form = SearchProduct(request.POST, error_class=ParagraphErrorList)
    if form.is_valid():
        item = request.GET['search']
        req = AllRequests()
        prd = req.search_product_item(item)
        print(item)
        product = prd.json()
        if not product['products']:
            context = {
                'user': user,
                'form': form,
                'badSearch': True
            }
            return render(request, 'store/result.html', context)
        product = product['products'][0]
        category_ = product['pnns_groups_2']
        picture = product['image_front_url']
        name = product['product_name']
        aProducts = ProductsNutriTypeA.objects.filter(category=category_)
        aProductl = []
        for prd in aProducts:
            aProductl.append(prd)
        paginator = Paginator(aProductl, 9)
        page = request.GET.get('page')
        try:
            pProducts = paginator.get_page(page)
        except PageNotAnInteger:
            pProducts = paginator.get_page(1)
        except EmptyPage:
            pProducts = paginator.get_page(paginator.num_pages)
        formi = SearchProduct()
        context = {'product': pProducts,
                   'picture': picture,
                   'name': name,
                   'form': formi,
                   'user': user,
                   'item': item
                   }
        logger.info('New search', exc_info=True, extra={
        # Optionally pass a request and we'll grab any information we can
        'request': request, })
        return render(request, 'store/result.html', context)


@login_required
def display_my_products(request):
    """display the favorite"""
    form = SearchProduct
    id_user = request.user.id
    user = get_object_or_404(User, pk=id_user)
    products = get_list_or_404(Favorite, id_user=user)
    favorite = []
    for prd in products:
        bdPrd = get_object_or_404(ProductsNutriTypeA, picture=prd.picture)
        favorite.append(bdPrd)
    paginator = Paginator(favorite, 9)
    page = request.GET.get('page')
    try:
        pProducts = paginator.get_page(page)
    except PageNotAnInteger:
        pProducts = paginator.get_page(1)
    except EmptyPage:
        pProducts = paginator.get_page(paginator.num_pages)
    context = {'products': pProducts,
               'form': form,
               'user': True
               }
    return render(request, 'store/show_products.html', context)


@login_required
def add_product_to_favorite(request, product_id):
    """Add product to favorite"""
    product = get_object_or_404(ProductsNutriTypeA, pk=product_id)
    id_user = request.user.id
    user = get_object_or_404(User, pk=id_user)
    name = product.product_name
    category = product.category
    picture = product.picture
    with transaction.atomic():
        prd = Favorite(name=name, generic_name=name, categorie=category, nutriscore='a', picture=picture,
                       id_user=user)
        prd.save()
    form = SearchProduct()
    context = {'form': form,
               'user': True,
               'name': name,
               'productAdd': True
               }
    return render(request, 'store/index.html', context)


def detail(request, id):
    """Display the product detail"""
    user = request.user.id
    if user:
        user = True
    else:
        user = False
    form = SearchProduct
    product = get_object_or_404(ProductsNutriTypeA, pk=id)
    code = product.code
    req = AllRequests()
    prod = req.code_request(code)
    product = prod.json()
    filtProduct = product['product']
    try:
        pictureFicheNutri = filtProduct['selected_images']['nutrition']['display']['fr']
    except KeyError:
        pictureFicheNutri = None
    filtProduct = product['product']
    try:
        picturePrd = filtProduct['image_front_url']
    except KeyError:
        picturePrd = None
    picture_nutri_score = 'https://static.openfoodfacts.org/images/misc/nutriscore-a.svg'
    name = filtProduct['product_name']
    context = {
        'nutri_score': picture_nutri_score,
        'nutri_pic': pictureFicheNutri,
        'code': code,
        'name': name,
        'form': form,
        'picture': picturePrd,
        'user': user
    }
    return render(request, 'store/detail.html', context)


def log_out(request):
    """Disconnect user"""
    logout(request)
    return HttpResponseRedirect('store/index.html')


def terms(request):
    """Display the terms of use"""
    form = SearchProduct
    return render(request, 'store/terms.html', context={'form': form})
