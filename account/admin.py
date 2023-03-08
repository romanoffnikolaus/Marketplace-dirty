from django.contrib import admin
from django.contrib.auth import get_user_model
# Register your models here.

User=get_user_model() #Так мы ссылаемся на юзера которого сами созлаем. Если импортировать юзера, то тогда он будет работать только с одной моделькой
# admin.site.register(User)

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('email', 'name', 'is_staff')
    list_filter = ['is_staff']