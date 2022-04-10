from django.shortcuts import render, get_object_or_404

from .forms import CommentForm
from .models import Category, Product, Gallery


def product_list(request, category_slug=None):
    category = None
    categories = Category.objects.all()
    products = Product.objects.filter(available=True)
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)
    return render(request, 'shop/index.html',
                  {'category': category,
                   'categories': categories,
                   'products': products})


def product_detail(request, id, slug):
    product = get_object_or_404(Product, id=id, slug=slug, available=True)
    gallery = Gallery.objects.filter(product=id)
    comments = product.comments.filter(active=True)
    return render(request, 'shop/detail.html',
                  {'product': product, 'gallery': gallery, 'comments': comments})


def product_comment(request, id, slug):
    product = get_object_or_404(Product, id=id, slug=slug, available=True)
    comments = product.comments.filter(active=True)
    gallery = Gallery.objects.filter(product=id)
    new_comment = None
    # Show 25 contacts per page.
    if request.method == 'POST' and 'add_comment' in request.POST:
        # Пользователь отправил комментарий.
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            # Создаем комментарий, но пока не сохраняем в базе данных.
            new_comment = comment_form.save(commit=False)
            new_comment.product_id = id
            # Привязываем комментарий к текущей статье.
            new_comment.post = product
            # Сохраняем комментарий в базе данных.
            new_comment.save()
    else:
        comment_form = CommentForm()
    return render(request, 'shop/comments.html',
                  {'product': product, 'gallery': gallery, 'comment_form': comment_form,
                   'comments': comments})
