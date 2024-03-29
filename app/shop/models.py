from django.db import models
from django.shortcuts import get_object_or_404
from django.urls import reverse


class Category(models.Model):
    name = models.CharField(max_length=200, db_index=True)
    slug = models.SlugField(max_length=200, unique=True)
    image = models.ImageField(upload_to=f'category', blank=True)

    class Meta:
        ordering = ('name',)
        verbose_name = 'category'
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return f'category/{self.name}'


class Brand(models.Model):
    name = models.CharField(max_length=50, db_index=True)

    def __str__(self):
        return self.name


class Ip(models.Model):
    ip = models.CharField(max_length=100)

    def __str__(self):
        return self.ip


class Product(models.Model):
    category = models.ForeignKey(Category,
                                 related_name='products',
                                 on_delete=models.CASCADE)
    name = models.CharField(max_length=200, db_index=True)
    slug = models.SlugField(max_length=200, db_index=True)
    brand = models.ForeignKey(Brand,
                              related_name='brands', null=True,
                              on_delete=models.SET_NULL)
    image = models.ImageField(upload_to='products', blank=True)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    available = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    ip_view = models.ManyToManyField(Ip, related_name="post_views", blank=True)

    class Meta:
        ordering = ('name',)
        index_together = (('id', 'slug'),)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('shop:product_detail', args=[self.id, self.slug])

    @property
    def get_rating(self):
        product = get_object_or_404(Product, id=self.id, available=True)
        comments = product.comments.filter(active=True)
        rating_list = [comment.rating for comment in comments]
        rating = round(sum(rating_list) / len(comments), 1)
        return rating

    @property
    def total_views(self):
        return self.ip_view.count()


class Gallery(models.Model):
    image = models.ImageField(upload_to='gallery')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')


class Comment(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='comments')
    name = models.CharField(max_length=80)
    email = models.EmailField()
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)
    rating = models.IntegerField(default=0)

    class Meta:
        ordering = ('created',)

    def __str__(self):
        return 'Comment by {} on {}'.format(self.name, self.product)
