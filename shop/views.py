from django.core import paginator
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render, get_object_or_404
from collections import Counter
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


def product_comment(request, id, slug, page_num):
    product = get_object_or_404(Product, id=id, slug=slug, available=True)
    comments_list = product.comments.filter(active=True)
    gallery = Gallery.objects.filter(product=id)
    rating_comments = [com.rating for com in comments_list]
    average_rating = sum(rating_comments) / len(comments_list)
    rating_comments = Counter(rating_comments)
    page_obj = Paginator(comments_list, 5)
    try:
        comments = page_obj.page(page_num)
    except PageNotAnInteger:
        # if page is not an integer, deliver the first page
        comments = page_obj.page(1)
    except EmptyPage:
        # if the page is out of range, deliver the last page
        comments = page_obj.page(paginator.num_pages)
    # Show 25 contacts per page.
    if request.method == 'POST':
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
    print(rating_comments, average_rating)
    return render(request, 'shop/comments.html',
                  {'product': product, 'gallery': gallery, 'comment_form': comment_form,
                   'comments': comments, 'rating_comments' : rating_comments, 'average_rating': average_rating })
