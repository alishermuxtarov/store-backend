from ckeditor.fields import RichTextField
from django.utils.translation import ugettext as _
from django.db import models

from authentication.models import User


class BaseModel(models.Model):
    created_date = models.DateField(auto_now_add=True, editable=False, verbose_name=_('Дата создания'), null=True)
    created_at = models.DateTimeField(auto_now_add=True, editable=False, verbose_name=_('Время создания'), null=True)
    updated_at = models.DateTimeField(auto_now=True, editable=False, verbose_name=_('Время обновления'), null=True)
    created_by = models.ForeignKey('authentication.User', models.SET_NULL, null=True, blank=True,
                                   related_name='created_%(class)ss', verbose_name=_('Создано пользоветем'))
    updated_by = models.ForeignKey('authentication.User', models.SET_NULL, null=True, blank=True,
                                   related_name='updated_%(class)ss', verbose_name=_('Обновлено пользоветем'))

    class Meta:
        abstract = True


class Category(BaseModel):
    name = models.CharField(_('Наименование'), max_length=255)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']
        verbose_name = _('Категория')
        verbose_name_plural = _('Категории')
        db_table = 'catalog_categories'


class Product(BaseModel):
    name = models.CharField(_('Наименование'), max_length=255)
    price = models.FloatField(_('Цена'), default=0.0)
    description = RichTextField(_('Описание'), max_length=10000)
    image = models.ImageField(upload_to='images/products', null=True)
    category = models.ForeignKey(Category, models.CASCADE, 'products', verbose_name=_('Категория'))

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['category', 'name']
        verbose_name = _('Товар')
        verbose_name_plural = _('Товары')
        db_table = 'catalog_products'


class Order(BaseModel):
    user = models.ForeignKey(User, models.CASCADE, 'orders', null=True, verbose_name=_('Пользователь'))
    email = models.EmailField(_('Email'))
    address = models.CharField(_('Адрес доставки'), max_length=255)

    def __str__(self):
        return 'Order #%d' % self.id

    class Meta:
        ordering = ['-id']
        verbose_name = _('Заказ')
        verbose_name_plural = _('Заказы')
        db_table = 'catalog_orders'


class OrderItem(BaseModel):
    order = models.ForeignKey(Order, models.CASCADE, 'items', verbose_name=_('Заказ'))
    product = models.ForeignKey(Product, models.CASCADE, 'order_items', verbose_name=_('Товар'))
    quantity = models.SmallIntegerField(_('Количество'))
    price = models.FloatField(_('Цена (Euro)'))
    amount = models.FloatField(_('Сумма'))

    def __str__(self):
        return 'Order item #%d' % self.id

    class Meta:
        ordering = ['id']
        verbose_name = _('Товар заказа')
        verbose_name_plural = _('Составляющие заказа')
        db_table = 'catalog_order_items'
