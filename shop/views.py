from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import render, get_object_or_404, redirect

from shop.forms import CommentModelForm, OrderModelForm, ProductModelForm
from shop.models import Product, Category, Comment


@login_required
def home(request, cat_id=None):
    categories = Category.objects.all()
    search = request.GET.get('search')
    comments = Comment.objects.all()
    if cat_id is not None:
        products = Product.objects.filter(category=cat_id)
    else:
        products = Product.objects.all()
    if search is not None:
        products = products.filter(Q(name__icontains=search) | Q(comments__full_name__icontains=search))
        comments = comments.filter(Q(comment__icontains=search) | Q(comments__full_name_icontains=search))
    context = {
        'categories': categories,
        'products': products,
        'comments': comments
    }
    return render(request, 'home.html', context)


@login_required
def detail(request, pk, cat_id=None):
    product = Product.objects.get(id=pk)
    categories = Category.objects.all()
    comments = product.comments.filter(is_active=True).order_by('-created_at')
    price_lower_bound = product.price*0.8
    price_upper_bound = product.price*1.2
    similar_products = Product.objects.filter(Q(price__lte=price_lower_bound) & Q(price__gte=price_upper_bound)).exclude(id=pk)
    count = product.comments.count()
    if cat_id is not None:
        products = Product.objects.filter(category=cat_id)
        return render(request, 'detail.html', {'products': products, })
    else:
        product = Product.objects.get(id=pk)
    context = {
        'product': product,
        'comments': comments,
        'count': count,
        'categories': categories,
        'similar_products': similar_products
    }
    return render(request, 'detail.html', context)
# def detail(request, pk, cat_id=None):
#     categories = Category.objects.all()
#     if cat_id is not None:
#         products = Product.objects.filter(category=cat_id)
#     else:
#         product = Product.objects.get(id=pk)
#         context = {
#             'product': product,
#             'categories': categories
#         }
#         return render(request, 'detail.html', context)


@login_required
def add_comment(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    if request.method == 'POST':
        form = CommentModelForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.product = product
            comment.save()
            return redirect('product_detail', product_id)

    else:
        form = CommentModelForm()
    context = {
        'form': form,
        'product': product
    }

    return render(request, 'detail.html', context)


@login_required
def order_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    form = OrderModelForm()

    if request.method == 'POST':

        form = OrderModelForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.product = product
            if product.quantity >= order.quantity:
                product.quantity -= order.quantity
                # add messaging
                product.save()
                order.save()
                messages.add_message(
                    request,
                    level=messages.SUCCESS,
                    message='Your order is successfully saved'
                )

                return redirect('product_detail', product_id)
            else:
                messages.add_message(
                    request,
                    level=messages.ERROR,
                    message='Your order is not available'
                )

    context = {
        'form': form,
        'product': product,
    }
    return render(request, 'detail.html', context)


@login_required
def add_product(request):
    form = ProductModelForm()
    if request.method == 'POST':
        form = ProductModelForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False)
            product.save()
            return redirect('home')
    else:
        form = ProductModelForm()
    return render(request, 'detail.html', {'form': form})


@login_required
def update_product(request, pk):
    product = get_object_or_404(Product, pk=pk)

    form = ProductModelForm(instance=product)
    if request.method == 'POST':
        form = ProductModelForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            return redirect('home', product.id)
    context = {
        'product': product,
        'form': form
    }
    return render(request, 'update_product.html', context)


@login_required
def delete_product(request, pk):
    product = get_object_or_404(Product, id=pk)
    if product:
        product.delete()
        return redirect('home')
    context = {
        'product': product
    }
    return render(request, 'detail.html', context)
