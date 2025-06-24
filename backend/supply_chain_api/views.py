from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db.models import Sum, Q
from datetime import datetime, timedelta
from .models import Supplier, Category, Product, PurchaseOrder, PurchaseOrderItem, Inventory
from .serializers import (
    SupplierSerializer, CategorySerializer, ProductSerializer,
    PurchaseOrderSerializer, PurchaseOrderItemSerializer, InventorySerializer
)


class SupplierViewSet(viewsets.ModelViewSet):
    queryset = Supplier.objects.all()
    serializer_class = SupplierSerializer
    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=['get'])
    def search(self, request):
        query = request.query_params.get('q', '')
        suppliers = self.queryset.filter(
            Q(name__icontains=query) | 
            Q(contact_person__icontains=query) |
            Q(phone__icontains=query)
        )
        serializer = self.get_serializer(suppliers, many=True)
        return Response(serializer.data)


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated]


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.select_related('supplier', 'category')
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=['get'])
    def low_stock(self, request):
        """获取库存不足的产品"""
        products = self.queryset.filter(
            stock_quantity__lte=models.F('min_stock_level')
        )
        serializer = self.get_serializer(products, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def search(self, request):
        query = request.query_params.get('q', '')
        products = self.queryset.filter(
            Q(name__icontains=query) | 
            Q(sku__icontains=query) |
            Q(description__icontains=query)
        )
        serializer = self.get_serializer(products, many=True)
        return Response(serializer.data)


class PurchaseOrderViewSet(viewsets.ModelViewSet):
    queryset = PurchaseOrder.objects.select_related('supplier', 'created_by')
    serializer_class = PurchaseOrderSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    @action(detail=True, methods=['post'])
    def approve(self, request, pk=None):
        """批准采购订单"""
        order = self.get_object()
        order.status = 'approved'
        order.save()
        serializer = self.get_serializer(order)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def ship(self, request, pk=None):
        """标记为已发货"""
        order = self.get_object()
        order.status = 'shipped'
        order.save()
        serializer = self.get_serializer(order)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def receive(self, request, pk=None):
        """标记为已收货"""
        order = self.get_object()
        order.status = 'received'
        order.save()
        
        # 更新产品库存
        for item in order.items.all():
            product = item.product
            product.stock_quantity += item.quantity
            product.save()
            
            # 更新或创建库存记录
            inventory, created = Inventory.objects.get_or_create(product=product)
            inventory.current_stock = product.stock_quantity
            inventory.save()
        
        serializer = self.get_serializer(order)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def dashboard(self, request):
        """获取采购订单仪表板数据"""
        total_orders = self.queryset.count()
        pending_orders = self.queryset.filter(status='pending').count()
        approved_orders = self.queryset.filter(status='approved').count()
        shipped_orders = self.queryset.filter(status='shipped').count()
        
        # 本月订单统计
        current_month = datetime.now().month
        current_year = datetime.now().year
        monthly_orders = self.queryset.filter(
            order_date__year=current_year,
            order_date__month=current_month
        ).count()
        
        # 总采购金额
        total_amount = self.queryset.aggregate(
            total=Sum('total_amount')
        )['total'] or 0
        
        return Response({
            'total_orders': total_orders,
            'pending_orders': pending_orders,
            'approved_orders': approved_orders,
            'shipped_orders': shipped_orders,
            'monthly_orders': monthly_orders,
            'total_amount': total_amount,
        })


class PurchaseOrderItemViewSet(viewsets.ModelViewSet):
    queryset = PurchaseOrderItem.objects.select_related('product', 'purchase_order')
    serializer_class = PurchaseOrderItemSerializer
    permission_classes = [IsAuthenticated]


class InventoryViewSet(viewsets.ModelViewSet):
    queryset = Inventory.objects.select_related('product')
    serializer_class = InventorySerializer
    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=['get'])
    def low_stock(self, request):
        """获取库存不足的产品"""
        inventories = self.queryset.filter(
            current_stock__lte=models.F('product__min_stock_level')
        )
        serializer = self.get_serializer(inventories, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def dashboard(self, request):
        """获取库存仪表板数据"""
        total_products = self.queryset.count()
        low_stock_products = self.queryset.filter(
            current_stock__lte=models.F('product__min_stock_level')
        ).count()
        
        total_stock_value = sum(
            inv.current_stock * inv.product.unit_price 
            for inv in self.queryset
        )
        
        return Response({
            'total_products': total_products,
            'low_stock_products': low_stock_products,
            'total_stock_value': total_stock_value,
        }) 