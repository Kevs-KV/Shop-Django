from collections import Counter

from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.views.generic import FormView, ListView

from .forms import CommentForm
from .models import Category, Product, Gallery, Comment


# def product_list(request, category_slug=None):
#     category = None
#     categories = Category.objects.all()
#     products = Product.objects.filter(available=True)
#     if category_slug:
#         category = get_object_or_404(Category, slug=category_slug)
#         products = products.filter(category=category)
#     return render(request, 'shop/index.html',
#                   {'category': category,
#                    'categories': categories,
#                    'products': products})

class ViewProductList(ListView):
    template_name = 'shop/index.html'
    model = Product

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, *kwargs)
        context['categories'] = Category.objects.all()
        print(context)
        return context

    def get_queryset(self):
        return Product.objects.filter(available=True)


def product_detail(request, id, slug):
    product = get_object_or_404(Product, id=id, slug=slug, available=True)
    gallery = Gallery.objects.filter(product=id)
    comments = product.comments.filter(active=True)
    return render(request, 'shop/detail.html',
                  {'product': product, 'gallery': gallery, 'comments': comments})


class ViewCreateProductComment(FormView):
    template_name = 'shop/comments.html'
    form_class = CommentForm
    paginate_by = 5
    model = Comment

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, *kwargs)
        kwargs = self.kwargs
        context['id'] = kwargs['id']
        context['slug'] = kwargs['slug']
        context['product'] = get_object_or_404(Product, id=context['id'], slug=context['slug'], available=True)
        context['comments_list'] = context['product'].comments.filter(active=True)
        context['gallery'] = Gallery.objects.filter(product=context['id'])
        context['rating_comments'] = [com.rating for com in context['comments_list']]
        context['average_rating'] = sum(context['rating_comments']) / len(context['comments_list'])
        context['len_comments_list'] = len(context['comments_list'])
        context['rating_comments'] = Counter(context['rating_comments'])

        return context

    def form_valid(self, form):
        new_comment = form.save(commit=False)
        context = self.get_context_data()
        new_comment.product_id = context['id']
        product = context['product']
        new_comment.post = product
        new_comment.save()

        return super().form_valid(form)

    def get_form(self, form_class=None):
        self.object = super().get_form(form_class)

        return self.object

    def get_success_url(self):
        context = self.get_context_data()

        return reverse('shop:product_comment', kwargs={'id': context['id'], 'slug': context['slug'], 'page_num': 1})

# def product_comment(request, id, slug, page_num):
#     product = get_object_or_404(Product, id=id, slug=slug, available=True)
#     comments_list = product.comments.filter(active=True)
#     gallery = Gallery.objects.filter(product=id)
#     rating_comments = [com.rating for com in comments_list]
#     average_rating = sum(rating_comments) / len(comments_list)
#     len_comments_list = len(comments_list)
#     rating_comments = Counter(rating_comments)
#     page_obj = Paginator(comments_list, 5)
#     try:
#         comments = page_obj.page(page_num)
#     except PageNotAnInteger:
#         # if page is not an integer, deliver the first page
#         comments = page_obj.page(1)
#     except EmptyPage:
#         # if the page is out of range, deliver the last page
#         comments = page_obj.page(paginator.num_pages)
#     # Show 25 contacts per page.
#     if request.method == 'POST':
#         # Пользователь отправил комментарий.
#         comment_form = CommentForm(data=request.POST)
#         if comment_form.is_valid():
#             # Создаем комментарий, но пока не сохраняем в базе данных.
#             new_comment = comment_form.save(commit=False)
#             new_comment.product_id = id
#             # Привязываем комментарий к текущей статье.
#             new_comment.post = product
#             # Сохраняем комментарий в базе данных.
#             new_comment.save()
#     else:
#         comment_form = CommentForm()
#     return render(request, 'shop/comments.html',
#                   {'product': product, 'gallery': gallery, 'comment_form': comment_form,
#                    'comments': comments, 'rating_comments': rating_comments, 'average_rating': average_rating,
#                    'len_comments_list': len_comments_list})
