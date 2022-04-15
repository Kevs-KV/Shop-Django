from collections import Counter

from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.views.generic import FormView, ListView, DetailView

from .forms import CommentForm
from .models import Category, Product, Gallery, Comment


class ViewProductList(ListView):
    template_name = 'shop/index.html'
    model = Product

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['categories'] = Category.objects.all()
        return context

    def get_queryset(self):
        return Product.objects.filter(available=True)


class ViewProductDetail(DetailView):
    template_name = 'shop/detail.html'
    model = Product

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        kwargs = self.kwargs
        context['product'] = get_object_or_404(Product, id=kwargs['id'], slug=kwargs['slug'], available=True)
        context['gallery'] = Gallery.objects.filter(product=kwargs['id'])
        context['comments'] = context['product'].comments.filter(active=True)
        return context


class ViewCreateProductComment(FormView):
    template_name = 'shop/comments.html'
    form_class = CommentForm
    paginate_by = 5
    model = Comment

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        kwargs = self.kwargs
        context['id'] = kwargs['id']
        context['slug'] = kwargs['slug']
        context['product'] = get_object_or_404(Product, id=context['id'], slug=context['slug'], available=True)
        context['comments_list'] = context['product'].comments.filter(active=True)
        context['gallery'] = Gallery.objects.filter(product=context['id'])
        context['rating_comments'] = [com.rating for com in context['comments_list']]
        context['average_rating'] = round(sum(context['rating_comments']) / len(context['comments_list']), 1)
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
