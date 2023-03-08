from django.contrib import admin
from django.urls import path,include
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
    openapi.Info(
        title='Lalavito',
        description='Маркетплейс написанный на втором хакатоне',
        default_version='v1'
    ), public= True
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('docs/', schema_view.with_ui('swagger')),
    path('', include('account.urls')),
    path('', include('marketplace_main.urls')),
]
