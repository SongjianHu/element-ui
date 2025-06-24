<template>
  <div class="low-stock-list">
    <div class="table-container">
      <div class="table-header">
        <h2 class="table-title">库存预警</h2>
        <div class="table-actions">
          <el-button type="primary" @click="$router.push('/inventory')">
            返回库存列表
          </el-button>
        </div>
      </div>

      <div v-if="lowStockProducts.length === 0" class="empty-state">
        <el-empty description="暂无库存预警" />
      </div>

      <el-table 
        v-else
        :data="lowStockProducts" 
        style="width: 100%" 
        v-loading="loading"
      >
        <el-table-column prop="sku" label="SKU" width="120" />
        <el-table-column prop="name" label="产品名称" min-width="200" />
        <el-table-column prop="category_name" label="分类" width="120" />
        <el-table-column prop="supplier_name" label="供应商" width="150" />
        <el-table-column prop="stock_quantity" label="当前库存" width="100">
          <template #default="scope">
            <span class="low-stock">{{ scope.row.stock_quantity }}</span>
          </template>
        </el-table-column>
        <el-table-column prop="min_stock_level" label="最低库存" width="100" />
        <el-table-column prop="unit_price" label="单价" width="100">
          <template #default="scope">
            ¥{{ formatCurrency(scope.row.unit_price) }}
          </template>
        </el-table-column>
        <el-table-column label="库存状态" width="120">
          <template #default="scope">
            <el-tag type="danger">
              库存不足
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column label="操作" width="200" fixed="right">
          <template #default="scope">
            <el-button size="small" @click="viewProduct(scope.row)">查看</el-button>
            <el-button size="small" type="primary" @click="createOrder(scope.row)">创建订单</el-button>
          </template>
        </el-table-column>
      </el-table>
    </div>

    <!-- 统计信息 -->
    <el-row :gutter="20" class="stats-row">
      <el-col :span="8">
        <div class="stat-card warning">
          <div class="stat-number">{{ lowStockProducts.length }}</div>
          <div class="stat-label">库存不足产品</div>
        </div>
      </el-col>
      <el-col :span="8">
        <div class="stat-card danger">
          <div class="stat-number">{{ zeroStockCount }}</div>
          <div class="stat-label">缺货产品</div>
        </div>
      </el-col>
      <el-col :span="8">
        <div class="stat-card info">
          <div class="stat-number">¥{{ formatCurrency(totalValue) }}</div>
          <div class="stat-label">库存总值</div>
        </div>
      </el-col>
    </el-row>
  </div>
</template>

<script>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import api from '@/api'
import { ElMessage } from 'element-plus'

export default {
  name: 'LowStockList',
  setup() {
    const router = useRouter()
    const loading = ref(false)
    const lowStockProducts = ref([])

    const zeroStockCount = computed(() => {
      return lowStockProducts.value.filter(product => product.stock_quantity === 0).length
    })

    const totalValue = computed(() => {
      return lowStockProducts.value.reduce((total, product) => {
        return total + (product.stock_quantity * product.unit_price)
      }, 0)
    })

    const fetchLowStockProducts = async () => {
      loading.value = true
      try {
        const response = await api.get('/products/low_stock/')
        lowStockProducts.value = response.data
      } catch (error) {
        ElMessage.error('获取库存预警数据失败')
      } finally {
        loading.value = false
      }
    }

    const viewProduct = (product) => {
      // 跳转到产品详情页
      console.log('查看产品:', product)
    }

    const createOrder = (product) => {
      // 跳转到创建订单页面，并预填产品信息
      router.push({
        path: '/purchase-orders/add',
        query: { 
          product_id: product.id,
          supplier_id: product.supplier
        }
      })
    }

    const formatCurrency = (amount) => {
      return Number(amount || 0).toLocaleString('zh-CN', {
        minimumFractionDigits: 2,
        maximumFractionDigits: 2
      })
    }

    onMounted(() => {
      fetchLowStockProducts()
    })

    return {
      loading,
      lowStockProducts,
      zeroStockCount,
      totalValue,
      viewProduct,
      createOrder,
      formatCurrency
    }
  }
}
</script>

<style scoped>
.low-stock-list {
  padding: 20px;
}

.table-container {
  background: #fff;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  padding: 20px;
  margin-bottom: 20px;
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

.empty-state {
  text-align: center;
  padding: 60px 0;
}

.stats-row {
  margin-bottom: 20px;
}

.stat-card {
  background: #fff;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  padding: 20px;
  text-align: center;
  border-left: 4px solid;
}

.stat-card.warning {
  border-left-color: #faad14;
}

.stat-card.danger {
  border-left-color: #ff4d4f;
}

.stat-card.info {
  border-left-color: #1890ff;
}

.stat-number {
  font-size: 24px;
  font-weight: bold;
  margin-bottom: 8px;
}

.stat-card.warning .stat-number {
  color: #faad14;
}

.stat-card.danger .stat-number {
  color: #ff4d4f;
}

.stat-card.info .stat-number {
  color: #1890ff;
}

.stat-label {
  font-size: 14px;
  color: #666;
}

.low-stock {
  color: #ff4d4f;
  font-weight: bold;
}
</style> 