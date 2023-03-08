from django.contrib import admin
from .models import Category, Stuffs, Rating, Comments, Order, Likes
from django.db.models import Avg
# Register your models here.

admin.site.register(Category)

class RatingInline(admin.TabularInline):
    model = Rating

@admin.register(Stuffs)
class StuffAdmin(admin.ModelAdmin):
    list_display = ('title', 'posted_at', 'price', 'quantity')
    inlines = [RatingInline]
    search_fields = ['title', 'posted_at']
    prepopulated_fields = {'slug': ('title',)}
    ordering = ['-posted_at']
    list_filter = ['category__title','posted_at', ]

    def get_rating(self, obj):
        result = obj.ratings.aggregate(Avg('rating'))
        return result['rating__avg']

@admin.register(Comments)
class CommentsAdmin(admin.ModelAdmin):
    list_display = ['stuff', 'author', 'body', 'posted_at']
    search_fields = ['stuff', 'posted_at']
    ordering = ['-posted_at']

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['order_number', 'user', 'shipping_address']
    search_fields = ['order_number', 'shipping_adress']
    list_filter = ['order_number', 'user']

