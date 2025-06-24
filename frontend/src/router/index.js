import { createRouter, createWebHistory } from 'vue-router'
import Dashboard from '@/views/Dashboard.vue'
import SupplierList from '@/views/suppliers/SupplierList.vue'
import SupplierForm from '@/views/suppliers/SupplierForm.vue'
import ProductList from '@/views/products/ProductList.vue'
import ProductForm from '@/views/products/ProductForm.vue'
import CategoryList from '@/views/categories/CategoryList.vue'
import PurchaseOrderList from '@/views/orders/PurchaseOrderList.vue'
import PurchaseOrderForm from '@/views/orders/PurchaseOrderForm.vue'
import InventoryList from '@/views/inventory/InventoryList.vue'
import LowStockList from '@/views/inventory/LowStockList.vue'

const routes = [
  {
    path: '/',
    redirect: '/dashboard'
  },
  {
    path: '/dashboard',
    name: 'Dashboard',
    component: Dashboard
  },
  {
    path: '/suppliers',
    name: 'SupplierList',
    component: SupplierList
  },
  {
    path: '/suppliers/add',
    name: 'SupplierAdd',
    component: SupplierForm
  },
  {
    path: '/suppliers/edit/:id',
    name: 'SupplierEdit',
    component: SupplierForm
  },
  {
    path: '/products',
    name: 'ProductList',
    component: ProductList
  },
  {
    path: '/products/add',
    name: 'ProductAdd',
    component: ProductForm
  },
  {
    path: '/products/edit/:id',
    name: 'ProductEdit',
    component: ProductForm
  },
  {
    path: '/categories',
    name: 'CategoryList',
    component: CategoryList
  },
  {
    path: '/purchase-orders',
    name: 'PurchaseOrderList',
    component: PurchaseOrderList
  },
  {
    path: '/purchase-orders/add',
    name: 'PurchaseOrderAdd',
    component: PurchaseOrderForm
  },
  {
    path: '/purchase-orders/edit/:id',
    name: 'PurchaseOrderEdit',
    component: PurchaseOrderForm
  },
  {
    path: '/inventory',
    name: 'InventoryList',
    component: InventoryList
  },
  {
    path: '/inventory/low-stock',
    name: 'LowStockList',
    component: LowStockList
  }
]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})

export default router 