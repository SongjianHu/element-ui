<template>
  <div class="inventory-list">
    <div class="table-container">
      <div class="table-header">
        <h2 class="table-title">库存管理</h2>
        <div class="table-actions">
          <el-button type="warning" @click="$router.push('/inventory/low-stock')">
            <el-icon><Warning /></el-icon>
            库存预警
          </el-button>
        </div>
      </div>

      <el-table 
        :data="inventory" 
        style="width: 100%" 
        v-loading="loading"
      >
        <el-table-column prop="product_sku" label="SKU" width="120" />
        <el-table-column prop="product_name" label="产品名称" min-width="200" />
        <el-table-column prop="current_stock" label="当前库存" width="100">
          <template #default="scope">
            <span :class="{ 'low-stock': isLowStock(scope.row) }">
              {{ scope.row.current_stock }}
            </span>
          </template>
        </el-table-column>
        <el-table-column prop="reserved_stock" label="预留库存" width="100" />
        <el-table-column prop="available_stock" label="可用库存" width="100">
          <template #default="scope">
            <span :class="{ 'low-stock': scope.row.available_stock <= 0 }">
              {{ scope.row.available_stock }}
            </span>
          </template>
        </el-table-column>
        <el-table-column prop="last_updated" label="最后更新" width="180">
          <template #default="scope">
            {{ formatDate(scope.row.last_updated) }}
          </template>
        </el-table-column>
        <el-table-column label="状态" width="100">
          <template #default="scope">
            <el-tag :type="getStockStatusType(scope.row)">
              {{ getStockStatusText(scope.row) }}
            </el-tag>
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

    <!-- 库存统计卡片 -->
    <el-row :gutter="20" class="stats-row">
      <el-col :span="8">
        <div class="stat-card">
          <div class="stat-number">{{ dashboardData.total_products || 0 }}</div>
          <div class="stat-label">产品总数</div>
        </div>
      </el-col>
      <el-col :span="8">
        <div class="stat-card">
          <div class="stat-number">{{ dashboardData.low_stock_products || 0 }}</div>
          <div class="stat-label">库存不足</div>
        </div>
      </el-col>
      <el-col :span="8">
        <div class="stat-card">
          <div class="stat-number">¥{{ formatCurrency(dashboardData.total_stock_value) }}</div>
          <div class="stat-label">库存总值</div>
        </div>
      </el-col>
    </el-row>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue'
import api from '@/api'
import { ElMessage } from 'element-plus'

export default {
  name: 'InventoryList',
  setup() {
    const loading = ref(false)
    const inventory = ref([])
    const currentPage = ref(1)
    const pageSize = ref(10)
    const total = ref(0)
    const dashboardData = ref({})

    const fetchInventory = async () => {
      loading.value = true
      try {
        const response = await api.get('/inventory/', {
          params: {
            page: currentPage.value,
            page_size: pageSize.value
          }
        })
        inventory.value = response.data.results || response.data
        total.value = response.data.count || response.data.length
      } catch (error) {
        ElMessage.error('获取库存列表失败')
      } finally {
        loading.value = false
      }
    }

    const fetchDashboardData = async () => {
      try {
        const response = await api.get('/inventory/dashboard/')
        dashboardData.value = response.data
      } catch (error) {
        ElMessage.error('获取库存统计数据失败')
      }
    }

    const handleSizeChange = (size) => {
      pageSize.value = size
      currentPage.value = 1
      fetchInventory()
    }

    const handleCurrentChange = (page) => {
      currentPage.value = page
      fetchInventory()
    }

    const formatDate = (dateString) => {
      if (!dateString) return ''
      return new Date(dateString).toLocaleString('zh-CN')
    }

    const formatCurrency = (amount) => {
      return Number(amount || 0).toLocaleString('zh-CN', {
        minimumFractionDigits: 2,
        maximumFractionDigits: 2
      })
    }

    const isLowStock = (item) => {
      // 这里需要根据产品的min_stock_level来判断
      // 由于API返回的数据结构，这里简化处理
      return item.current_stock <= 10
    }

    const getStockStatusType = (item) => {
      if (item.available_stock <= 0) return 'danger'
      if (isLowStock(item)) return 'warning'
      return 'success'
    }

    const getStockStatusText = (item) => {
      if (item.available_stock <= 0) return '缺货'
      if (isLowStock(item)) return '库存不足'
      return '正常'
    }

    onMounted(() => {
      fetchInventory()
      fetchDashboardData()
    })

    return {
      loading,
      inventory,
      currentPage,
      pageSize,
      total,
      dashboardData,
      handleSizeChange,
      handleCurrentChange,
      formatDate,
      formatCurrency,
      isLowStock,
      getStockStatusType,
      getStockStatusText
    }
  }
}
</script>

<style scoped>
.inventory-list {
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

.table-footer {
  margin-top: 20px;
  display: flex;
  justify-content: flex-end;
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
}

.stat-number {
  font-size: 24px;
  font-weight: bold;
  color: #409EFF;
  margin-bottom: 8px;
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