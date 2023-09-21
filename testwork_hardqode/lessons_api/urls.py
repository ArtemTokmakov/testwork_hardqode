from django.urls import path
from .views import (
    get_lessons_for_user,
    get_lessons_for_product,
    get_product_statistics)

urlpatterns = [
    path('api/lessons/',
         get_lessons_for_user,
         name='get_lessons_for_user'),
    path('api/lessons/<int:product_id>/',
         get_lessons_for_product,
         name='get_lessons_for_product'),
    path('api/product-statistics/',
         get_product_statistics,
         name='get_product_statistics'),
]
