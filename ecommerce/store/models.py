from django.db import models
from django.contrib.auth.models import User


class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True, verbose_name="Пользователь")
    name = models.CharField(max_length=255, null=True, verbose_name="Название")
    email = models.CharField(max_length=255, null=True, verbose_name="E-mail")

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=255, null=True, verbose_name="Название")
    price = models.FloatField(verbose_name="Цена")
    digital = models.BooleanField(default=False, null=True, blank=False)
    image = models.ImageField(null=True, blank=True, verbose_name="Фото")

    def __str__(self):
        return self.name

    @property
    def imageURL(self):
        try:
            url = self.image.url
        except:
            url = ''
        return url


class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True,
                                 verbose_name="Пользователь")
    data_added = models.DateTimeField(auto_now_add=True, verbose_name="Время добавления")
    complete = models.BooleanField(default=False, null=True, blank=False)
    transaction_id = models.CharField(max_length=255, null=True)

    def __str__(self):
        return str(self.id)

    @property
    def shipping(self):
        shipping = False
        orderitems = self.orderitem_set.all()
        for i in orderitems:
            if i.product.digital == False:
                shipping = True
        return shipping

    @property
    def get_cart_total(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.get_total for item in orderitems])
        return total

    @property
    def get_cart_items(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.quantity for item in orderitems])
        return total


class OrderItem(models.Model):
    product = models.ForeignKey(Product, null=True, blank=True, on_delete=models.CASCADE, verbose_name="Продукт")
    order = models.ForeignKey(Order, null=True, blank=True, on_delete=models.SET_NULL, verbose_name="Заказ")
    quantity = models.IntegerField(default=0, null=True, blank=True, verbose_name="Кол-во")
    data_added = models.DateTimeField(auto_now_add=True, verbose_name="Время добавления")

    def __str__(self):
        return str(self.id)

    @property
    def get_total(self):
        total = self.product.price * self.quantity
        return total


class ShippingAddress(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True,
                                 verbose_name="Пользователь")
    order = models.ForeignKey(Order, null=True, blank=True, on_delete=models.SET_NULL, verbose_name="Заказ")
    address = models.CharField(max_length=255, null=True, verbose_name="Адрес")
    email = models.CharField(max_length=255, null=True, verbose_name="E-mail")
    city = models.CharField(max_length=255, null=True, verbose_name="Город")
    zipcode = models.CharField(max_length=255, null=True, verbose_name="Индекс")
    data_added = models.DateTimeField(auto_now_add=True, verbose_name="Время добавления")

    def __str__(self):
        return self.address
