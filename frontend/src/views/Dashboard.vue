<template>
  <div class="dashboard">
    <el-row :gutter="20" class="stats-row">
      <el-col :span="6">
        <div class="stat-card" style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);">
          <div class="stat-number">{{ dashboardData.total_orders || 0 }}</div>
          <div class="stat-label">总订单数</div>
        </div>
      </el-col>
      <el-col :span="6">
        <div class="stat-card" style="background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);">
          <div class="stat-number">{{ dashboardData.pending_orders || 0 }}</div>
          <div class="stat-label">待处理订单</div>
        </div>
      </el-col>
      <el-col :span="6">
        <div class="stat-card" style="background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);">
          <div class="stat-number">{{ dashboardData.total_products || 0 }}</div>
          <div class="stat-label">产品总数</div>
        </div>
      </el-col>
      <el-col :span="6">
        <div class="stat-card" style="background: linear-gradient(135deg, #43e97b 0%, #38f9d7 100%);">
          <div class="stat-number">¥{{ formatCurrency(dashboardData.total_amount) }}</div>
          <div class="stat-label">总采购金额</div>
        </div>
      </el-col>
    </el-row>

    <el-row :gutter="20" class="charts-row">
      <el-col :span="12">
        <div class="dashboard-card">
          <div class="card-header">
            <h3 class="card-title">订单状态分布</h3>
          </div>
          <div class="chart-container">
            <el-progress 
              :percentage="getOrderStatusPercentage('pending')" 
              :color="'#fa8c16'"
              :stroke-width="20"
            >
              <span>待处理: {{ dashboardData.pending_orders || 0 }}</span>
            </el-progress>
            <el-progress 
              :percentage="getOrderStatusPercentage('approved')" 
              :color="'#52c41a'"
              :stroke-width="20"
            >
              <span>已批准: {{ dashboardData.approved_orders || 0 }}</span>
            </el-progress>
            <el-progress 
              :percentage="getOrderStatusPercentage('shipped')" 
              :color="'#1890ff'"
              :stroke-width="20"
            >
              <span>已发货: {{ dashboardData.shipped_orders || 0 }}</span>
            </el-progress>
            <el-progress 
              :percentage="getOrderStatusPercentage('received')" 
              :color="'#722ed1'"
              :stroke-width="20"
            >
              <span>已收货: {{ dashboardData.received_orders || 0 }}</span>
            </el-progress>
          </div>
        </div>
      </el-col>
      
      <el-col :span="12">
        <div class="dashboard-card">
          <div class="card-header">
            <h3 class="card-title">库存预警</h3>
            <el-button type="primary" size="small" @click="$router.push('/inventory/low-stock')">
              查看详情
            </el-button>
          </div>
          <div class="low-stock-list">
            <div v-if="lowStockProducts.length === 0" class="empty-state">
              <el-empty description="暂无库存预警" />
            </div>
            <div v-else>
              <div v-for="product in lowStockProducts.slice(0, 5)" :key="product.id" class="low-stock-item">
                <div class="product-info">
                  <div class="product-name">{{ product.name }}</div>
                  <div class="product-sku">{{ product.sku }}</div>
                </div>
                <div class="stock-info">
                  <span class="current-stock">{{ product.stock_quantity }}</span>
                  <span class="min-stock">/ {{ product.min_stock_level }}</span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </el-col>
    </el-row>

    <el-row :gutter="20" class="recent-orders-row">
      <el-col :span="24">
        <div class="dashboard-card">
          <div class="card-header">
            <h3 class="card-title">最近订单</h3>
            <el-button type="primary" size="small" @click="$router.push('/purchase-orders')">
              查看全部
            </el-button>
          </div>
          <el-table :data="recentOrders" style="width: 100%" v-loading="loading">
            <el-table-column prop="order_number" label="订单编号" width="150" />
            <el-table-column prop="supplier_name" label="供应商" width="200" />
            <el-table-column prop="order_date" label="订单日期" width="120" />
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
            <el-table-column label="操作" width="150">
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
              </template>
            </el-table-column>
          </el-table>
        </div>
      </el-col>
    </el-row>
  </div>
</template>

<script>
import { ref, onMounted, computed } from 'vue'
import { useStore } from 'vuex'
import api from '@/api'
import { ElMessage } from 'element-plus'

export default {
  name: 'Dashboard',
  setup() {
    const store = useStore()
    const loading = ref(false)
    const dashboardData = ref({})
    const lowStockProducts = ref([])
    const recentOrders = ref([])

    const fetchDashboardData = async () => {
      loading.value = true
      try {
        const [ordersResponse, productsResponse, lowStockResponse] = await Promise.all([
          api.get('/purchase-orders/dashboard/'),
          api.get('/products/'),
          api.get('/products/low_stock/')
        ])
        
        dashboardData.value = ordersResponse.data
        lowStockProducts.value = lowStockResponse.data
        recentOrders.value = ordersResponse.data.recent_orders || []
      } catch (error) {
        ElMessage.error('获取仪表板数据失败')
      } finally {
        loading.value = false
      }
    }

    const getOrderStatusPercentage = (status) => {
      const total = dashboardData.value.total_orders || 1
      const count = dashboardData.value[`${status}_orders`] || 0
      return Math.round((count / total) * 100)
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

    const viewOrder = (order) => {
      // 跳转到订单详情页
      console.log('查看订单:', order)
    }

    const approveOrder = async (order) => {
      try {
        await api.post(`/purchase-orders/${order.id}/approve/`)
        ElMessage.success('订单已批准')
        fetchDashboardData()
      } catch (error) {
        ElMessage.error('批准订单失败')
      }
    }

    onMounted(() => {
      fetchDashboardData()
    })

    return {
      loading,
      dashboardData,
      lowStockProducts,
      recentOrders,
      getOrderStatusPercentage,
      formatCurrency,
      getStatusType,
      getStatusText,
      viewOrder,
      approveOrder
    }
  }
}
</script>

<style scoped>
.dashboard {
  padding: 20px;
}

.stats-row {
  margin-bottom: 20px;
}

.stat-card {
  color: white;
  border-radius: 8px;
  padding: 20px;
  text-align: center;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
}

.stat-number {
  font-size: 32px;
  font-weight: bold;
  margin-bottom: 8px;
}

.stat-label {
  font-size: 14px;
  opacity: 0.9;
}

.charts-row {
  margin-bottom: 20px;
}

.chart-container {
  padding: 20px 0;
}

.chart-container .el-progress {
  margin-bottom: 16px;
}

.low-stock-list {
  max-height: 300px;
  overflow-y: auto;
}

.low-stock-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 12px 0;
  border-bottom: 1px solid #f0f0f0;
}

.low-stock-item:last-child {
  border-bottom: none;
}

.product-info {
  flex: 1;
}

.product-name {
  font-weight: 500;
  color: #333;
}

.product-sku {
  font-size: 12px;
  color: #999;
  margin-top: 4px;
}

.stock-info {
  text-align: right;
}

.current-stock {
  font-size: 18px;
  font-weight: bold;
  color: #ff4d4f;
}

.min-stock {
  font-size: 12px;
  color: #999;
}

.empty-state {
  text-align: center;
  padding: 40px 0;
}

.recent-orders-row {
  margin-bottom: 20px;
}

@media (max-width: 768px) {
  .stats-row .el-col {
    margin-bottom: 16px;
  }
  
  .stat-number {
    font-size: 24px;
  }
}
</style> 