from django.db import models
import json
import datetime


class User(models.Model):
    user_email = models.CharField("Email", max_length=40, default="NULL")
    user_password_hash = models.TextField("Хэш пароля", max_length=200, default="NULL")


class FoodCourt(models.Model):
    foodcourt_name = models.CharField("Название", max_length=30, default="NULL")
    foodcourt_width = models.CharField("Широта", max_length=40, default="NULL")
    foodcourt_longitude = models.CharField("Долгота", max_length=40, default="NULL")
    #foodcourt_address = models.CharField("Адрес", max_length=30, default="NULL")


class Restaurant(models.Model):
    restaurant_name = models.CharField("Название", max_length=30, default="NULL")
    restaurant_description = models.TextField("Описание", max_length=200, default="NULL")
    restaurant_rating = models.IntegerField("Оценка", default=0)
    restaurant_foodcourt = models.ForeignKey("FoodCourt", on_delete=models.CASCADE, default=1)
    restaurant_image = models.ImageField("Картинка", upload_to="restaurantimages/")


class Dish(models.Model):
    dish_name = models.CharField("Название", max_length=30, default="NULL")
    dish_category = models.CharField("Категория", max_length=20, default="NULL")
    dish_description = models.TextField("Описание", max_length=200, default="NULL")
    dish_price = models.FloatField("Цена", default=0)
    dish_image = models.ImageField("Картинка", upload_to="dish_images/")
    dish_restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)


class Order(models.Model):
    static_order_number = 1
    order_restautant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    order_number = models.IntegerField("Номер заказа", default=-1)
    order_dish = models.ForeignKey(Dish, on_delete=models.CASCADE)
    order_quantity = models.IntegerField("Количество блюд", default= -1)
    order_date = models.DateTimeField(auto_now_add=True)
    order_user = models.ForeignKey(User, on_delete=models.CASCADE)
    order_status = models.CharField("Статус заказа", max_length=30, default="NULL")




