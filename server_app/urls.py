from django.urls import path, include
import django.contrib.auth.urls

from rest_framework.urlpatterns import format_suffix_patterns
from . import views

urlpatterns = [
    path("index/", views.index, name="index"),
    path("add_dish/", views.add_dish, name="add_dish"),
    path("get_dishes/", views.get_all_dishes, name="get_dishes"),
    path("get_image/", views.get_image, name="Получение картинки"),
    path("delete_dish/", views.delete_dish, name="Удаление блюд"),
    path("get_restaurant_dishes/", views.get_restaurant_dishes, name="Получить блюда из ресторана"),
    path("get_all_restaurants/", views.get_all_restaurants, name="Получение списка ресторанов"),
    path("create_restaurant/", views.create_restaurant, name="Добавление ресторана"),
    path("get_foodcourt_restaurants/", views.get_foodcourt_restaurants, name="Получение списка ресторанов фудкорта"),
    path("create_order/", views.create_order, name="Создание заказа")
]

