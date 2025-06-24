from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator


class Supplier(models.Model):
    """供应商模型"""
    name = models.CharField(max_length=200, verbose_name='供应商名称')
    contact_person = models.CharField(max_length=100, verbose_name='联系人')
    phone = models.CharField(max_length=20, verbose_name='联系电话')
    email = models.EmailField(verbose_name='邮箱')
    address = models.TextField(verbose_name='地址')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        verbose_name = '供应商'
        verbose_name_plural = '供应商'

    def __str__(self):
        return self.name


class Category(models.Model):
    """产品分类模型"""
    name = models.CharField(max_length=100, verbose_name='分类名称')
    description = models.TextField(blank=True, verbose_name='分类描述')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')

    class Meta:
        verbose_name = '产品分类'
        verbose_name_plural = '产品分类'

    def __str__(self):
        return self.name


class Product(models.Model):
    """产品模型"""
    name = models.CharField(max_length=200, verbose_name='产品名称')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='产品分类')
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE, verbose_name='供应商')
    sku = models.CharField(max_length=50, unique=True, verbose_name='SKU编码')
    description = models.TextField(blank=True, verbose_name='产品描述')
    unit_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='单价')
    stock_quantity = models.IntegerField(default=0, validators=[MinValueValidator(0)], verbose_name='库存数量')
    min_stock_level = models.IntegerField(default=0, validators=[MinValueValidator(0)], verbose_name='最低库存水平')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        verbose_name = '产品'
        verbose_name_plural = '产品'

    def __str__(self):
        return self.name


class PurchaseOrder(models.Model):
    """采购订单模型"""
    ORDER_STATUS_CHOICES = [
        ('pending', '待处理'),
        ('approved', '已批准'),
        ('shipped', '已发货'),
        ('received', '已收货'),
        ('cancelled', '已取消'),
    ]

    order_number = models.CharField(max_length=50, unique=True, verbose_name='订单编号')
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE, verbose_name='供应商')
    order_date = models.DateField(verbose_name='订单日期')
    expected_delivery_date = models.DateField(verbose_name='预计交货日期')
    status = models.CharField(max_length=20, choices=ORDER_STATUS_CHOICES, default='pending', verbose_name='订单状态')
    total_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0, verbose_name='订单总金额')
    notes = models.TextField(blank=True, verbose_name='备注')
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='创建人')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        verbose_name = '采购订单'
        verbose_name_plural = '采购订单'

    def __str__(self):
        return self.order_number


class PurchaseOrderItem(models.Model):
    """采购订单项目模型"""
    purchase_order = models.ForeignKey(PurchaseOrder, on_delete=models.CASCADE, related_name='items', verbose_name='采购订单')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='产品')
    quantity = models.IntegerField(validators=[MinValueValidator(1)], verbose_name='数量')
    unit_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='单价')
    total_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='总价')

    class Meta:
        verbose_name = '采购订单项目'
        verbose_name_plural = '采购订单项目'

    def save(self, *args, **kwargs):
        self.total_price = self.quantity * self.unit_price
        super().save(*args, **kwargs)


class Inventory(models.Model):
    """库存模型"""
    product = models.OneToOneField(Product, on_delete=models.CASCADE, verbose_name='产品')
    current_stock = models.IntegerField(default=0, validators=[MinValueValidator(0)], verbose_name='当前库存')
    reserved_stock = models.IntegerField(default=0, validators=[MinValueValidator(0)], verbose_name='预留库存')
    available_stock = models.IntegerField(default=0, validators=[MinValueValidator(0)], verbose_name='可用库存')
    last_updated = models.DateTimeField(auto_now=True, verbose_name='最后更新时间')

    class Meta:
        verbose_name = '库存'
        verbose_name_plural = '库存'

    def save(self, *args, **kwargs):
        self.available_stock = self.current_stock - self.reserved_stock
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.product.name} - 库存: {self.current_stock}" 