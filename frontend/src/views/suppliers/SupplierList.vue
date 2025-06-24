<template>
  <div class="supplier-list">
    <div class="table-container">
      <div class="table-header">
        <h2 class="table-title">供应商管理</h2>
        <div class="table-actions">
          <el-input
            v-model="searchQuery"
            placeholder="搜索供应商..."
            style="width: 300px; margin-right: 16px;"
            clearable
            @input="handleSearch"
          >
            <template #prefix>
              <el-icon><Search /></el-icon>
            </template>
          </el-input>
          <el-button type="primary" @click="$router.push('/suppliers/add')">
            <el-icon><Plus /></el-icon>
            添加供应商
          </el-button>
        </div>
      </div>

      <el-table 
        :data="filteredSuppliers" 
        style="width: 100%" 
        v-loading="loading"
        @selection-change="handleSelectionChange"
      >
        <el-table-column type="selection" width="55" />
        <el-table-column prop="name" label="供应商名称" min-width="200" />
        <el-table-column prop="contact_person" label="联系人" width="120" />
        <el-table-column prop="phone" label="联系电话" width="150" />
        <el-table-column prop="email" label="邮箱" width="200" />
        <el-table-column prop="address" label="地址" min-width="250" show-overflow-tooltip />
        <el-table-column prop="created_at" label="创建时间" width="180">
          <template #default="scope">
            {{ formatDate(scope.row.created_at) }}
          </template>
        </el-table-column>
        <el-table-column label="操作" width="200" fixed="right">
          <template #default="scope">
            <el-button size="small" @click="viewSupplier(scope.row)">查看</el-button>
            <el-button size="small" type="primary" @click="editSupplier(scope.row)">编辑</el-button>
            <el-button size="small" type="danger" @click="deleteSupplier(scope.row)">删除</el-button>
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

    <!-- 供应商详情对话框 -->
    <el-dialog v-model="detailDialogVisible" title="供应商详情" width="600px">
      <div v-if="selectedSupplier" class="supplier-detail">
        <el-descriptions :column="2" border>
          <el-descriptions-item label="供应商名称">{{ selectedSupplier.name }}</el-descriptions-item>
          <el-descriptions-item label="联系人">{{ selectedSupplier.contact_person }}</el-descriptions-item>
          <el-descriptions-item label="联系电话">{{ selectedSupplier.phone }}</el-descriptions-item>
          <el-descriptions-item label="邮箱">{{ selectedSupplier.email }}</el-descriptions-item>
          <el-descriptions-item label="地址" :span="2">{{ selectedSupplier.address }}</el-descriptions-item>
          <el-descriptions-item label="创建时间">{{ formatDate(selectedSupplier.created_at) }}</el-descriptions-item>
          <el-descriptions-item label="更新时间">{{ formatDate(selectedSupplier.updated_at) }}</el-descriptions-item>
        </el-descriptions>
      </div>
    </el-dialog>
  </div>
</template>

<script>
import { ref, onMounted, computed } from 'vue'
import { useStore } from 'vuex'
import api from '@/api'
import { ElMessage, ElMessageBox } from 'element-plus'

export default {
  name: 'SupplierList',
  setup() {
    const store = useStore()
    const loading = ref(false)
    const suppliers = ref([])
    const searchQuery = ref('')
    const currentPage = ref(1)
    const pageSize = ref(10)
    const total = ref(0)
    const selectedSuppliers = ref([])
    const detailDialogVisible = ref(false)
    const selectedSupplier = ref(null)

    const filteredSuppliers = computed(() => {
      if (!searchQuery.value) return suppliers.value
      return suppliers.value.filter(supplier => 
        supplier.name.toLowerCase().includes(searchQuery.value.toLowerCase()) ||
        supplier.contact_person.toLowerCase().includes(searchQuery.value.toLowerCase()) ||
        supplier.phone.includes(searchQuery.value)
      )
    })

    const fetchSuppliers = async () => {
      loading.value = true
      try {
        const response = await api.get('/suppliers/', {
          params: {
            page: currentPage.value,
            page_size: pageSize.value
          }
        })
        suppliers.value = response.data.results || response.data
        total.value = response.data.count || response.data.length
      } catch (error) {
        ElMessage.error('获取供应商列表失败')
      } finally {
        loading.value = false
      }
    }

    const handleSearch = () => {
      currentPage.value = 1
      fetchSuppliers()
    }

    const handleSelectionChange = (selection) => {
      selectedSuppliers.value = selection
    }

    const handleSizeChange = (size) => {
      pageSize.value = size
      currentPage.value = 1
      fetchSuppliers()
    }

    const handleCurrentChange = (page) => {
      currentPage.value = page
      fetchSuppliers()
    }

    const viewSupplier = (supplier) => {
      selectedSupplier.value = supplier
      detailDialogVisible.value = true
    }

    const editSupplier = (supplier) => {
      store.$router.push(`/suppliers/edit/${supplier.id}`)
    }

    const deleteSupplier = async (supplier) => {
      try {
        await ElMessageBox.confirm(
          `确定要删除供应商 "${supplier.name}" 吗？`,
          '确认删除',
          {
            confirmButtonText: '确定',
            cancelButtonText: '取消',
            type: 'warning'
          }
        )
        
        await api.delete(`/suppliers/${supplier.id}/`)
        ElMessage.success('供应商删除成功')
        fetchSuppliers()
      } catch (error) {
        if (error !== 'cancel') {
          ElMessage.error('删除供应商失败')
        }
      }
    }

    const formatDate = (dateString) => {
      if (!dateString) return ''
      return new Date(dateString).toLocaleString('zh-CN')
    }

    onMounted(() => {
      fetchSuppliers()
    })

    return {
      loading,
      suppliers,
      searchQuery,
      currentPage,
      pageSize,
      total,
      selectedSuppliers,
      detailDialogVisible,
      selectedSupplier,
      filteredSuppliers,
      handleSearch,
      handleSelectionChange,
      handleSizeChange,
      handleCurrentChange,
      viewSupplier,
      editSupplier,
      deleteSupplier,
      formatDate
    }
  }
}
</script>

<style scoped>
.supplier-list {
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

.supplier-detail {
  padding: 20px 0;
}
</style> 