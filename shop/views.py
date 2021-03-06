from django.shortcuts import render, get_object_or_404
from .models import Category, Product, ProductImage
from cart.forms import CartAddProductForm
from django.core.paginator import Paginator


def product_list(request, category_slug=None):
    category = None
    categories = Category.objects.all()
    products = Product.objects.filter(available=True)

    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)

    # ------------------------------paginator
    paginator = Paginator(products, 4)

    page_number = request.GET.get('page', 1)
    page = paginator.get_page(page_number)

    is_paginated = page.has_other_pages()

    if page.has_previous():
        prev_url = '?page={}'.format(page.previous_page_number())
    else:
        prev_url = ''

    if page.has_next():
        next_url = '?page={}'.format(page.next_page_number())
    else:
        next_url = ''
    # ------------------------------
    context = {'category': category,
               'categories': categories,
               'products': page,
               'is_paginated': is_paginated,
               'next_url': next_url,
               'prev_url': prev_url}

    return render(request, 'shop/product/list.html', context)


def product_detail(request, id, slug):
    product = get_object_or_404(Product, id=id, slug=slug, available=True)
    cart_product_form = CartAddProductForm()
    return render(request, 'shop/product/detail.html',
                  {'product': product,
                   'cart_product_form': cart_product_form})


def StartPageViews(request):
    category = 1
    context = {'category': category}

    return render(request, 'shop/StartPage.html', context)
