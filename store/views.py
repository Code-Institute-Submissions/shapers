from django.shortcuts import render, get_object_or_404
from .models import Product
from django.db.models import Q
from django.core.paginator import Paginator


def store(request):
    """View returning the Store landing page"""

    products = Product.objects.all()

    query_string = None
    query_categories = None
    query_sorting = None

    # Keep products per page %3 aligned with BS grid
    per_page = 9
    p = Paginator(products, per_page=per_page)

    if request.GET:

        if 'category' in request.GET:
            query_categories = request.GET['category'].split(',')
            products = products.filter(category__name__in=query_categories)
            request.session['search_category'] = query_categories

        elif 'search_category' in request.session:
            products = products.filter(
                category__name__in=request.session['search_category'])

        if 'q' in request.GET:
            query_string = request.GET['q']
            queries = Q(name__icontains=query_string) | Q(
                description__icontains=query_string)
            products = products.filter(queries)

        if 'sort' in request.GET:
            sort = request.GET['sort']
            sort_by = sort
            if sort_by == 'price':
                sort_by = 'base_price'
            elif sort_by == 'date':
                sort_by = 'date_version'

            if 'direction' in request.GET:
                sort_direction = request.GET['direction']
                if sort_direction == 'desc':
                    sort_by = f'-{sort_by}'
                query_sorting = f'{sort}_{sort_direction}'
            products = products.order_by(sort_by)

            request.session['sort_by'] = sort_by

        elif 'sort_by' in request.session:
            products = products.order_by(request.session['sort_by'])

        p = Paginator(products, per_page=per_page)

        if 'page' in request.GET:
            page = p.get_page(request.GET['page'])
        else:
            page = p.get_page(1)
    else:
        page = p.get_page(1)

    context = {
        'products': products,
        'query_string': query_string,
        'query_categories': query_categories,
        'query_sorting': query_sorting,
        'page': page,
    }

    return render(request, 'store/store.html', context=context)


def product_details(request, product_id):
    """View returning a product details"""

    product = get_object_or_404(Product, pk=product_id)

    context = {
        'product': product
    }

    return render(request, 'store/product_details.html', context=context)
