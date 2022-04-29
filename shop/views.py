from collections import Counter

from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.views.generic import FormView, ListView, DetailView
from cart.cart import Cart
from cart.forms import CartAddProductForm
from .forms import CommentForm
from .models import Category, Product, Gallery, Comment, Brand


class GetCategoryBrand:

    def get_category(self):
        return Category.objects.all()

    def get_brand(self):
        return Brand.objects.all()


class ViewProductList(ListView):
    template_name = 'shop/product_detail/index.html'
    model = Product

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['cart_product_form'] = CartAddProductForm()
        return context

    def get_queryset(self):
        return Product.objects.filter(available=True)


class ViewProductDetail(DetailView):
    template_name = 'shop/product_detail/detail.html'
    model = Product

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        kwargs = self.kwargs
        context['cart_product_form'] = CartAddProductForm()
        context['product'] = get_object_or_404(Product, id=kwargs['id'], slug=kwargs['slug'], available=True)
        context['gallery'] = Gallery.objects.filter(product=kwargs['id'])
        context['comments'] = context['product'].comments.filter(active=True)
        return context


class ViewCreateProductComment(FormView):
    template_name = 'shop/product_detail/comments.html'
    form_class = CommentForm
    paginate_by = 5
    model = Comment

    def get_context_data(self, **kwargs):
        context = super(ViewCreateProductComment, self).get_context_data(**kwargs)
        kwargs = self.kwargs
        context['id'] = kwargs['id']
        context['page_num'] = kwargs['page_num']
        context['slug'] = kwargs['slug']
        context['product'] = get_object_or_404(Product, id=context['id'], slug=context['slug'], available=True)
        comments_list = context['product'].comments.filter(active=True)
        paginator = Paginator(comments_list, self.paginate_by)
        page = paginator.get_page(kwargs['page_num'])
        context['page'] = page
        context['comments_list'] = page.object_list
        context['gallery'] = Gallery.objects.filter(product=context['id'])
        context['rating_comments'] = [comment.rating for comment in comments_list]
        try:
            context['average_rating'] = round(sum(context['rating_comments']) / len(comments_list), 1)
        except ZeroDivisionError:
            context['average_rating'] = 0
        context['len_comments_list'] = len(comments_list)
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


class ViewProductListForCategory(GetCategoryBrand, ListView):
    template_name = 'shop/store.html'
    model = Product
    paginate_by = 9

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        return context

    def get_queryset(self):
        return Product.objects.filter(available=True)


class ViewFilterProductList(ViewProductListForCategory):

    def get_queryset(self):
        price_min = self.request.GET.get('price-min')
        price_max = self.request.GET.get('price-max')
        return Product.objects.filter(Q(category__name__in=self.request.GET.getlist('category')) |
                                      Q(brand__name__in=self.request.GET.getlist('brand'))).filter(
            price__range=(price_min, price_max))
