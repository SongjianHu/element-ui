<template>
  <div class="purchase-order-list">
    <div class="table-container">
      <div class="table-header">
        <h2 class="table-title">采购订单</h2>
        <div class="table-actions">
          <el-button type="primary" @click="$router.push('/purchase-orders/add')">
            <el-icon><Plus /></el-icon>
            创建订单
          </el-button>
        </div>
      </div>

      <el-table 
        :data="orders" 
        style="width: 100%" 
        v-loading="loading"
      >
        <el-table-column prop="order_number" label="订单编号" width="150" />
        <el-table-column prop="supplier_name" label="供应商" width="200" />
        <el-table-column prop="order_date" label="订单日期" width="120">
          <template #default="scope">
            {{ formatDate(scope.row.order_date) }}
          </template>
        </el-table-column>
        <el-table-column prop="expected_delivery_date" label="预计交货" width="120">
          <template #default="scope">
            {{ formatDate(scope.row.expected_delivery_date) }}
          </template>
        </el-table-column>
        <el-table-column prop="total_amount" label="订单金额" width="120">
          <template #default="scope">
            ¥{{ formatCurrency(scope.row.total_amount) }}
          </template>
        </el-table-column>
        <el-table-column prop="status" label="状态" width="100">
          <template #default="scope">
            <el-tag :type="getStatusType(scope.row.status)">
              {{ getStatusText(scope.row.status) }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="created_by_name" label="创建人" width="100" />
        <el-table-column label="操作" width="200" fixed="right">
          <template #default="scope">
            <el-button size="small" @click="viewOrder(scope.row)">查看</el-button>
            <el-button 
              v-if="scope.row.status === 'pending'" 
              size="small" 
              type="success" 
              @click="approveOrder(scope.row)"
            >
              批准
            </el-button>
            <el-button 
              v-if="scope.row.status === 'approved'" 
              size="small" 
              type="primary" 
              @click="shipOrder(scope.row)"
            >
              发货
            </el-button>
            <el-button 
              v-if="scope.row.status === 'shipped'" 
              size="small" 
              type="warning" 
              @click="receiveOrder(scope.row)"
            >
              收货
            </el-button>
          </template>
        </el-table-column>
      </el-table>

      <div class="table-footer">
        <el-pagination
          v-model:current-page="currentPage"
          v-model:page-size="pageSize"
          :page-sizes="[10, 20, 50, 100]"
          :total="total"
          layout="total, sizes, prev, pager, next, jumper"
          @size-change="handleSizeChange"
          @current-change="handleCurrentChange"
        />
      </div>
    </div>

    <!-- 订单详情对话框 -->
    <el-dialog v-model="detailDialogVisible" title="订单详情" width="800px">
      <div v-if="selectedOrder" class="order-detail">
        <el-descriptions :column="2" border>
          <el-descriptions-item label="订单编号">{{ selectedOrder.order_number }}</el-descriptions-item>
          <el-descriptions-item label="供应商">{{ selectedOrder.supplier_name }}</el-descriptions-item>
          <el-descriptions-item label="订单日期">{{ formatDate(selectedOrder.order_date) }}</el-descriptions-item>
          <el-descriptions-item label="预计交货">{{ formatDate(selectedOrder.expected_delivery_date) }}</el-descriptions-item>
          <el-descriptions-item label="订单状态">
            <el-tag :type="getStatusType(selectedOrder.status)">
              {{ getStatusText(selectedOrder.status) }}
            </el-tag>
          </el-descriptions-item>
          <el-descriptions-item label="订单金额">¥{{ formatCurrency(selectedOrder.total_amount) }}</el-descriptions-item>
          <el-descriptions-item label="创建人">{{ selectedOrder.created_by_name }}</el-descriptions-item>
          <el-descriptions-item label="创建时间">{{ formatDate(selectedOrder.created_at) }}</el-descriptions-item>
          <el-descriptions-item label="备注" :span="2">{{ selectedOrder.notes || '无' }}</el-descriptions-item>
        </el-descriptions>

        <div class="order-items">
          <h4>订单项目</h4>
          <el-table :data="selectedOrder.items" style="width: 100%">
            <el-table-column prop="product_name" label="产品名称" />
            <el-table-column prop="product_sku" label="SKU" width="120" />
            <el-table-column prop="quantity" label="数量" width="80" />
            <el-table-column prop="unit_price" label="单价" width="100">
              <template #default="scope">
                ¥{{ formatCurrency(scope.row.unit_price) }}
              </template>
            </el-table-column>
            <el-table-column prop="total_price" label="总价" width="100">
              <template #default="scope">
                ¥{{ formatCurrency(scope.row.total_price) }}
              </template>
            </el-table-column>
          </el-table>
        </div>
      </div>
    </el-dialog>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue'
import api from '@/api'
import { ElMessage, ElMessageBox } from 'element-plus'

export default {
  name: 'PurchaseOrderList',
  setup() {
    const loading = ref(false)
    const orders = ref([])
    const currentPage = ref(1)
    const pageSize = ref(10)
    const total = ref(0)
    const detailDialogVisible = ref(false)
    const selectedOrder = ref(null)

    const fetchOrders = async () => {
      loading.value = true
      try {
        const response = await api.get('/purchase-orders/', {
          params: {
            page: currentPage.value,
            page_size: pageSize.value
          }
        })
        orders.value = response.data.results || response.data
        total.value = response.data.count || response.data.length
      } catch (error) {
        ElMessage.error('获取订单列表失败')
      } finally {
        loading.value = false
      }
    }

    const handleSizeChange = (size) => {
      pageSize.value = size
      currentPage.value = 1
      fetchOrders()
    }

    const handleCurrentChange = (page) => {
      currentPage.value = page
      fetchOrders()
    }

    const viewOrder = (order) => {
      selectedOrder.value = order
      detailDialogVisible.value = true
    }

    const approveOrder = async (order) => {
      try {
        await ElMessageBox.confirm('确定要批准这个订单吗？', '确认批准', {
          confirmButtonText: '确定',
          cancelButtonText: '取消',
          type: 'warning'
        })
        
        await api.post(`/purchase-orders/${order.id}/approve/`)
        ElMessage.success('订单已批准')
        fetchOrders()
      } catch (error) {
        if (error !== 'cancel') {
          ElMessage.error('批准订单失败')
        }
      }
    }

    const shipOrder = async (order) => {
      try {
        await ElMessageBox.confirm('确定要标记为已发货吗？', '确认发货', {
          confirmButtonText: '确定',
          cancelButtonText: '取消',
          type: 'warning'
        })
        
        await api.post(`/purchase-orders/${order.id}/ship/`)
        ElMessage.success('订单已标记为发货')
        fetchOrders()
      } catch (error) {
        if (error !== 'cancel') {
          ElMessage.error('标记发货失败')
        }
      }
    }

    const receiveOrder = async (order) => {
      try {
        await ElMessageBox.confirm('确定要标记为已收货吗？这将更新产品库存。', '确认收货', {
          confirmButtonText: '确定',
          cancelButtonText: '取消',
          type: 'warning'
        })
        
        await api.post(`/purchase-orders/${order.id}/receive/`)
        ElMessage.success('订单已标记为收货，库存已更新')
        fetchOrders()
      } catch (error) {
        if (error !== 'cancel') {
          ElMessage.error('标记收货失败')
        }
      }
    }

    const formatDate = (dateString) => {
      if (!dateString) return ''
      return new Date(dateString).toLocaleDateString('zh-CN')
    }

    const formatCurrency = (amount) => {
      return Number(amount || 0).toLocaleString('zh-CN', {
        minimumFractionDigits: 2,
        maximumFractionDigits: 2
      })
    }

    const getStatusType = (status) => {
      const typeMap = {
        'pending': 'warning',
        'approved': 'success',
        'shipped': 'primary',
        'received': 'success',
        'cancelled': 'danger'
      }
      return typeMap[status] || 'info'
    }

    const getStatusText = (status) => {
      const textMap = {
        'pending': '待处理',
        'approved': '已批准',
        'shipped': '已发货',
        'received': '已收货',
        'cancelled': '已取消'
      }
      return textMap[status] || status
    }

    onMounted(() => {
      fetchOrders()
    })

    return {
      loading,
      orders,
      currentPage,
      pageSize,
      total,
      detailDialogVisible,
      selectedOrder,
      handleSizeChange,
      handleCurrentChange,
      viewOrder,
      approveOrder,
      shipOrder,
      receiveOrder,
      formatDate,
      formatCurrency,
      getStatusType,
      getStatusText
    }
  }
}
</script>

<style scoped>
.purchase-order-list {
  padding: 20px;
}

.table-container {
  background: #fff;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  padding: 20px;
}

.table-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.table-title {
  font-size: 20px;
  font-weight: 600;
  color: #333;
  margin: 0;
}

.table-actions {
  display: flex;
  align-items: center;
}

.table-footer {
  margin-top: 20px;
  display: flex;
  justify-content: flex-end;
}

.order-detail {
  padding: 20px 0;
}

.order-items {
  margin-top: 20px;
}

.order-items h4 {
  margin-bottom: 16px;
  color: #333;
}
</style> 