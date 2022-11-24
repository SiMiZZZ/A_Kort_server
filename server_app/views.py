import json
from django.shortcuts import render
from django.http import HttpResponse
from .models import *
from django.core import serializers
from django.template import RequestContext
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import base64
from django.core.files.base import ContentFile
import os

from rest_framework import generics

def index(request):
    return HttpResponse("Тестовая страница")


@csrf_exempt
def add_dish(request): #добавление нового блюда в меню
    data = json.loads(request.body.decode())["dish"]
    new_dish = Dish()
    new_dish.dish_name = data["dish_name"]
    new_dish.dish_price = data["dish_price"]
    new_dish.dish_description = data["dish_description"]
    new_dish.dish_category = data["dish_category"]
    name = data["restaurant_name"]
    address = data["restaurant_location"]
    foodcourt = FoodCourt.objects.all().filter(foodcourt_name=address)[0]
    new_dish.dish_restaurant = Restaurant.objects.all().filter(restaurant_name=name).filter(restaurant_foodcourt=foodcourt)[0]

    # Код по сохранению фото
    if "dish_image" in data.keys():
        format, imgstr = dict(data)["dish_image"].split(';base64,')
        ext = format.split('/')[-1]
        data_file = ContentFile(base64.b64decode(imgstr), name='temp.' + ext)
        file_name = "'{}.".format(hash(new_dish.dish_name)) + ext
        new_dish.dish_image.save(file_name, data_file, save=True)

    print(new_dish.dish_image.name)
    new_dish.save()
    return HttpResponse("ОК")


def get_all_dishes(request): #Получение всех блюд, лежащих в базе
    dishes = Dish.objects.all()
    if len(dishes)<1:
        return HttpResponse(json.dumps({}))
    return_dict = {"dishes": []}
    for dish in dishes:
        dish_dict = {}
        dish_dict["dish_name"] = dish.dish_name
        dish_dict["dish_price"] = dish.dish_price
        dish_dict["dish_description"] = dish.dish_description
        dish_dict["dish_category"] = dish.dish_category
        dish_dict["dish_image"] = str(dish.dish_image)
        return_dict["dishes"].append(dish_dict)
    json_dict = json.dumps(return_dict)
    return HttpResponse(json_dict)



def get_image(request): #получение картинки по ссылке
    file_location = "./media/{0}".format(request.GET.get("image"))
    with open(file_location, "rb") as f:
        file_data = f.read()
    return HttpResponse(file_data, content_type="image/png")


def delete_dish(request): #Удаление блюда из базы
    name = request.GET.get("name")
    dish_image_name = Dish.objects.all().filter(dish_name=name)[0].dish_image
    if dish_image_name != "":
        file_location = "./media/{0}".format(dish_image_name)
        os.remove(file_location)
    Dish.objects.filter(dish_name=name).delete()
    return HttpResponse("ОК")


def get_restaurant_dishes(request): # Получение блюд из определенного ресторана с GET-параметрами (name, address)
    name = request.GET.get("name")
    address = request.GET.get("address")
    print(name, address)
    foodcourt = FoodCourt.objects.all().filter(foodcourt_name=address)[0]
    restaurant = Restaurant.objects.all().filter(restaurant_name=name).filter(restaurant_foodcourt=foodcourt)[0]
    dishes = Dish.objects.all().filter(dish_restaurant=restaurant)
    if len(dishes) < 1:
        return HttpResponse(json.dumps({}))
    return_dict = {"dishes": []}
    for dish in dishes:
        dish_dict = {}
        dish_dict["dish_name"] = dish.dish_name
        dish_dict["dish_price"] = dish.dish_price
        dish_dict["dish_description"] = dish.dish_description
        dish_dict["dish_category"] = dish.dish_category
        dish_dict["dish_image"] = str(dish.dish_image)
        return_dict["dishes"].append(dish_dict)
    json_dict = json.dumps(return_dict)
    return HttpResponse(json_dict)


def get_all_restaurants(request):
        restaurants = Restaurant.objects.all()
        return_dict = {"restaurants": []}
        for restaurant in restaurants:
            dish_dict = {}
            dish_dict["name"] = restaurant.restaurant_name
            dish_dict["description"] = restaurant.restaurant_description
            dish_dict["location"] = restaurant.restaurant_foodcourt.foodcourt_name
            dish_dict["img"] = str(restaurant.restaurant_image)
            return_dict["restaurants"].append(dish_dict)
        json_dict = json.dumps(return_dict)
        return HttpResponse(json_dict)


def get_foodcourt_restaurants(request): #Получение рестаранов из данного фурдкорта(по имени фудкорта)
    name = request.GET.get("name")
    foodcourt = FoodCourt.objects.all().filter(foodcourt_name=name)[0]
    restaurants = Restaurant.objects.all().filter(restaurant_foodcourt=foodcourt)
    return_dict = {"restaurants": []}
    for restaurant in restaurants:
        restaurant_dict = {}
        restaurant_dict["name"] = restaurant.restaurant_name
        restaurant_dict["description"] = restaurant.restaurant_description
        restaurant_dict["location"] = restaurant.restaurant_foodcourt.foodcourt_name
        restaurant_dict["img"] = str(restaurant.restaurant_image)
        restaurant_dict["rating"] = restaurant.restaurant_rating
        return_dict["restaurants"].append(restaurant_dict)
    json_dict = json.dumps(return_dict)
    return HttpResponse(json_dict)

@csrf_exempt
def create_restaurant(request): #Создание ресторана
    restaurant = Restaurant()
    data = dict(json.loads(request.body.decode()))
    restaurant.restaurant_name = data["name"]
    restaurant.restaurant_description = data["description"]
    restaurant.restaurant_foodcourt = FoodCourt.objects.all().filter(foodcourt_name=data["location"])[0]
    restaurant.save()
    # Код по сохранению фото
    if "img" in data.keys():
        format, imgstr = dict(data)["img"].split(';base64,')
        ext = format.split('/')[-1]
        data_file = ContentFile(base64.b64decode(imgstr), name='temp.' + ext)
        file_name = "'{}.".format(hash(restaurant.restaurant_name)) + ext
        restaurant.restaurant_image.save(file_name, data_file, save=True)

    return HttpResponse("ОК")



@csrf_exempt
def create_order(request): #Создание заказа
    data = dict(json.loads(request.body.decode()))
    foodcourt = FoodCourt.objects.all().filter(foodcourt_name=data["restaurant_location"])[0]
    restautant = Restaurant.objects.all().filter(restaurant_name=data["restaurant_name"])\
                .filter(restaurant_foodcourt=foodcourt)[0]
    order_number = Order.static_order_number
    Order.static_order_number+= 1
    for dish in data['dishes']:
        new_order = Order()
        new_order.order_restautant = restautant
        new_order.order_dish = Dish.objects.all().filter(dish_restaurant=restautant).filter(dish_name=dish['name'])[0]
        new_order.order_number = order_number
        new_order.save()

    return HttpResponse("ОК")




