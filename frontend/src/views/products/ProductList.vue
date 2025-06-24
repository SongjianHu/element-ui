<template>
  <div class="product-list">
    <div class="table-container">
      <div class="table-header">
        <h2 class="table-title">产品管理</h2>
        <div class="table-actions">
          <el-input
            v-model="searchQuery"
            placeholder="搜索产品..."
            style="width: 300px; margin-right: 16px;"
            clearable
            @input="handleSearch"
          >
            <template #prefix>
              <el-icon><Search /></el-icon>
            </template>
          </el-input>
          <el-button type="primary" @click="$router.push('/products/add')">
            <el-icon><Plus /></el-icon>
            添加产品
          </el-button>
        </div>
      </div>

      <el-table 
        :data="filteredProducts" 
        style="width: 100%" 
        v-loading="loading"
      >
        <el-table-column prop="sku" label="SKU" width="120" />
        <el-table-column prop="name" label="产品名称" min-width="200" />
        <el-table-column prop="category_name" label="分类" width="120" />
        <el-table-column prop="supplier_name" label="供应商" width="150" />
        <el-table-column prop="unit_price" label="单价" width="100">
          <template #default="scope">
            ¥{{ formatCurrency(scope.row.unit_price) }}
          </template>
        </el-table-column>
        <el-table-column prop="stock_quantity" label="库存" width="100">
          <template #default="scope">
            <span :class="{ 'low-stock': isLowStock(scope.row) }">
              {{ scope.row.stock_quantity }}
            </span>
          </template>
        </el-table-column>
        <el-table-column prop="min_stock_level" label="最低库存" width="100" />
        <el-table-column label="操作" width="200" fixed="right">
          <template #default="scope">
            <el-button size="small" @click="viewProduct(scope.row)">查看</el-button>
            <el-button size="small" type="primary" @click="editProduct(scope.row)">编辑</el-button>
            <el-button size="small" type="danger" @click="deleteProduct(scope.row)">删除</el-button>
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

    <!-- 产品详情对话框 -->
    <el-dialog v-model="detailDialogVisible" title="产品详情" width="700px">
      <div v-if="selectedProduct" class="product-detail">
        <el-descriptions :column="2" border>
          <el-descriptions-item label="SKU">{{ selectedProduct.sku }}</el-descriptions-item>
          <el-descriptions-item label="产品名称">{{ selectedProduct.name }}</el-descriptions-item>
          <el-descriptions-item label="产品分类">{{ selectedProduct.category_name }}</el-descriptions-item>
          <el-descriptions-item label="供应商">{{ selectedProduct.supplier_name }}</el-descriptions-item>
          <el-descriptions-item label="单价">¥{{ formatCurrency(selectedProduct.unit_price) }}</el-descriptions-item>
          <el-descriptions-item label="库存数量">{{ selectedProduct.stock_quantity }}</el-descriptions-item>
          <el-descriptions-item label="最低库存">{{ selectedProduct.min_stock_level }}</el-descriptions-item>
          <el-descriptions-item label="创建时间">{{ formatDate(selectedProduct.created_at) }}</el-descriptions-item>
          <el-descriptions-item label="产品描述" :span="2">{{ selectedProduct.description || '暂无描述' }}</el-descriptions-item>
        </el-descriptions>
      </div>
    </el-dialog>
  </div>
</template>

<script>
import { ref, onMounted, computed } from 'vue'
import { useRouter } from 'vue-router'
import api from '@/api'
import { ElMessage, ElMessageBox } from 'element-plus'

export default {
  name: 'ProductList',
  setup() {
    const router = useRouter()
    const loading = ref(false)
    const products = ref([])
    const searchQuery = ref('')
    const currentPage = ref(1)
    const pageSize = ref(10)
    const total = ref(0)
    const detailDialogVisible = ref(false)
    const selectedProduct = ref(null)

    const filteredProducts = computed(() => {
      if (!searchQuery.value) return products.value
      return products.value.filter(product => 
        product.name.toLowerCase().includes(searchQuery.value.toLowerCase()) ||
        product.sku.toLowerCase().includes(searchQuery.value.toLowerCase()) ||
        product.description?.toLowerCase().includes(searchQuery.value.toLowerCase())
      )
    })

    const fetchProducts = async () => {
      loading.value = true
      try {
        const response = await api.get('/products/', {
          params: {
            page: currentPage.value,
            page_size: pageSize.value
          }
        })
        products.value = response.data.results || response.data
        total.value = response.data.count || response.data.length
      } catch (error) {
        ElMessage.error('获取产品列表失败')
      } finally {
        loading.value = false
      }
    }

    const handleSearch = () => {
      currentPage.value = 1
      fetchProducts()
    }

    const handleSizeChange = (size) => {
      pageSize.value = size
      currentPage.value = 1
      fetchProducts()
    }

    const handleCurrentChange = (page) => {
      currentPage.value = page
      fetchProducts()
    }

    const viewProduct = (product) => {
      selectedProduct.value = product
      detailDialogVisible.value = true
    }

    const editProduct = (product) => {
      router.push(`/products/edit/${product.id}`)
    }

    const deleteProduct = async (product) => {
      try {
        await ElMessageBox.confirm(
          `确定要删除产品 "${product.name}" 吗？`,
          '确认删除',
          {
            confirmButtonText: '确定',
            cancelButtonText: '取消',
            type: 'warning'
          }
        )
        
        await api.delete(`/products/${product.id}/`)
        ElMessage.success('产品删除成功')
        fetchProducts()
      } catch (error) {
        if (error !== 'cancel') {
          ElMessage.error('删除产品失败')
        }
      }
    }

    const formatCurrency = (amount) => {
      return Number(amount || 0).toLocaleString('zh-CN', {
        minimumFractionDigits: 2,
        maximumFractionDigits: 2
      })
    }

    const formatDate = (dateString) => {
      if (!dateString) return ''
      return new Date(dateString).toLocaleString('zh-CN')
    }

    const isLowStock = (product) => {
      return product.stock_quantity <= product.min_stock_level
    }

    onMounted(() => {
      fetchProducts()
    })

    return {
      loading,
      products,
      searchQuery,
      currentPage,
      pageSize,
      total,
      detailDialogVisible,
      selectedProduct,
      filteredProducts,
      handleSearch,
      handleSizeChange,
      handleCurrentChange,
      viewProduct,
      editProduct,
      deleteProduct,
      formatCurrency,
      formatDate,
      isLowStock
    }
  }
}
</script>

<style scoped>
.product-list {
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

.product-detail {
  padding: 20px 0;
}

.low-stock {
  color: #ff4d4f;
  font-weight: bold;
}
</style> 