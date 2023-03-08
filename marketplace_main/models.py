from django.db import models
from django.contrib.auth import get_user_model
from slugify import slugify
from PIL import Image
# Create your models here.
User = get_user_model()


class Category(models.Model):
    title = models.CharField(max_length=30, unique=True)
    slug = models.SlugField(max_length=30, primary_key=True, blank=True)

    def __str__(self) -> str:
        return self.title
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save()


class Stuffs(models.Model):
    title = models.CharField(max_length=30)
    descriptinon = models.TextField()
    image = models.ImageField(upload_to='stuffs_image/', blank=True)
    slug = models.SlugField(max_length=30, primary_key=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='stuffs')
    posted_at = models.DateField(auto_now_add=True)
    price = models.IntegerField()
    quantity = models.IntegerField()
    seller = models.ForeignKey(User, on_delete=models.CASCADE, related_name='stuffs')

    def __str__(self) -> str:
        return self.title
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save()
    
    class Meta:
        verbose_name = 'Stuff'
        verbose_name_plural = "Stuffs"


class Rating(models.Model):
    author = models.ForeignKey(User,on_delete=models.CASCADE, related_name='ratings')
    rating = models.PositiveSmallIntegerField()
    stuff = models.ForeignKey(Stuffs, on_delete=models.CASCADE, related_name='ratings')

    def __str__(self) -> str:
        return f'Stuff: {self.stuff} - Rating: {self.rating}'

    class Meta:
        verbose_name = 'Rating'
        verbose_name_plural = "Rating"


class Comments(models.Model):
    author = models.ForeignKey(User,on_delete=models.CASCADE, related_name='comments')
    stuff = models.ForeignKey(Stuffs, on_delete=models.CASCADE, related_name='comments')
    body = models.TextField()
    posted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.body
    
    class Meta:
        verbose_name = 'Comment'
        verbose_name_plural = "Commentaries"


class Favorites(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='favorites')
    product = models.ForeignKey(Stuffs, on_delete=models.CASCADE)
    favorites = models.BooleanField(default=False)
    
    def __str__(self) -> str:
        return self.product


class Likes(models.Model): 
    author = models.ForeignKey(User,on_delete=models.CASCADE, related_name='likes')
    stuff = models.ForeignKey(Stuffs, on_delete=models.CASCADE, related_name='likes')
    is_liked = models.BooleanField(default=False)

    def __str__(self) -> str:
        return f'Лайk от: {self.author}'
# Лайки реализованы формально для соответствия требованиям.


class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    products = models.ForeignKey(Stuffs, on_delete=models.CASCADE, related_name='products_in_cart')
    quantity = models.IntegerField(default=1)
    price = models.BigIntegerField(default=0)


    def __str__(self):
        return self.products.title


class Order(models.Model):
    order_number = models.CharField(max_length=5)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    product = models.ForeignKey(Stuffs, on_delete=models.CASCADE, related_name='orders')
    shipping_address = models.CharField(max_length=150, blank=False)

    def __str__(self) -> str:
        return self.product