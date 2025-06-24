<template>
  <div class="category-list">
    <div class="table-container">
      <div class="table-header">
        <h2 class="table-title">产品分类管理</h2>
        <div class="table-actions">
          <el-button type="primary" @click="showAddDialog = true">
            <el-icon><Plus /></el-icon>
            添加分类
          </el-button>
        </div>
      </div>

      <el-table 
        :data="categories" 
        style="width: 100%" 
        v-loading="loading"
      >
        <el-table-column prop="name" label="分类名称" min-width="200" />
        <el-table-column prop="description" label="分类描述" min-width="300" show-overflow-tooltip />
        <el-table-column prop="created_at" label="创建时间" width="180">
          <template #default="scope">
            {{ formatDate(scope.row.created_at) }}
          </template>
        </el-table-column>
        <el-table-column label="操作" width="200" fixed="right">
          <template #default="scope">
            <el-button size="small" type="primary" @click="editCategory(scope.row)">编辑</el-button>
            <el-button size="small" type="danger" @click="deleteCategory(scope.row)">删除</el-button>
          </template>
        </el-table-column>
      </el-table>
    </div>

    <!-- 添加/编辑分类对话框 -->
    <el-dialog 
      v-model="showAddDialog" 
      :title="editingCategory ? '编辑分类' : '添加分类'"
      width="500px"
    >
      <el-form 
        ref="formRef" 
        :model="form" 
        :rules="rules" 
        label-width="100px"
      >
        <el-form-item label="分类名称" prop="name">
          <el-input v-model="form.name" placeholder="请输入分类名称" />
        </el-form-item>
        
        <el-form-item label="分类描述" prop="description">
          <el-input 
            v-model="form.description" 
            type="textarea" 
            :rows="3"
            placeholder="请输入分类描述" 
          />
        </el-form-item>
      </el-form>
      
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="showAddDialog = false">取消</el-button>
          <el-button type="primary" @click="handleSubmit" :loading="submitting">
            {{ editingCategory ? '更新' : '创建' }}
          </el-button>
        </span>
      </template>
    </el-dialog>
  </div>
</template>

<script>
import { ref, reactive, onMounted } from 'vue'
import api from '@/api'
import { ElMessage, ElMessageBox } from 'element-plus'

export default {
  name: 'CategoryList',
  setup() {
    const loading = ref(false)
    const submitting = ref(false)
    const categories = ref([])
    const showAddDialog = ref(false)
    const editingCategory = ref(null)
    const formRef = ref()
    
    const form = reactive({
      name: '',
      description: ''
    })
    
    const rules = {
      name: [
        { required: true, message: '请输入分类名称', trigger: 'blur' },
        { min: 2, max: 100, message: '长度在 2 到 100 个字符', trigger: 'blur' }
      ],
      description: [
        { max: 500, message: '描述不能超过500个字符', trigger: 'blur' }
      ]
    }
    
    const fetchCategories = async () => {
      loading.value = true
      try {
        const response = await api.get('/categories/')
        categories.value = response.data
      } catch (error) {
        ElMessage.error('获取分类列表失败')
      } finally {
        loading.value = false
      }
    }
    
    const resetForm = () => {
      form.name = ''
      form.description = ''
      editingCategory.value = null
      if (formRef.value) {
        formRef.value.resetFields()
      }
    }
    
    const editCategory = (category) => {
      editingCategory.value = category
      form.name = category.name
      form.description = category.description
      showAddDialog.value = true
    }
    
    const deleteCategory = async (category) => {
      try {
        await ElMessageBox.confirm(
          `确定要删除分类 "${category.name}" 吗？`,
          '确认删除',
          {
            confirmButtonText: '确定',
            cancelButtonText: '取消',
            type: 'warning'
          }
        )
        
        await api.delete(`/categories/${category.id}/`)
        ElMessage.success('分类删除成功')
        fetchCategories()
      } catch (error) {
        if (error !== 'cancel') {
          ElMessage.error('删除分类失败')
        }
      }
    }
    
    const handleSubmit = async () => {
      if (!formRef.value) return
      
      try {
        await formRef.value.validate()
        submitting.value = true
        
        if (editingCategory.value) {
          await api.put(`/categories/${editingCategory.value.id}/`, form)
          ElMessage.success('分类更新成功')
        } else {
          await api.post('/categories/', form)
          ElMessage.success('分类创建成功')
        }
        
        showAddDialog.value = false
        resetForm()
        fetchCategories()
      } catch (error) {
        if (error !== false) {
          ElMessage.error(editingCategory.value ? '更新失败' : '创建失败')
        }
      } finally {
        submitting.value = false
      }
    }
    
    const formatDate = (dateString) => {
      if (!dateString) return ''
      return new Date(dateString).toLocaleString('zh-CN')
    }
    
    onMounted(() => {
      fetchCategories()
    })
    
    return {
      loading,
      submitting,
      categories,
      showAddDialog,
      editingCategory,
      formRef,
      form,
      rules,
      editCategory,
      deleteCategory,
      handleSubmit,
      formatDate
    }
  }
}
</script>

<style scoped>
.category-list {
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

.dialog-footer {
  display: flex;
  justify-content: flex-end;
  gap: 12px;
}
</style> 