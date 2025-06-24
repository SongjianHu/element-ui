<template>
  <div class="product-form">
    <div class="form-container">
      <h2 class="form-title">{{ isEdit ? '编辑产品' : '添加产品' }}</h2>
      
      <el-form 
        ref="formRef" 
        :model="form" 
        :rules="rules" 
        label-width="120px"
        @submit.prevent="handleSubmit"
      >
        <el-form-item label="产品名称" prop="name">
          <el-input v-model="form.name" placeholder="请输入产品名称" />
        </el-form-item>
        
        <el-form-item label="SKU编码" prop="sku">
          <el-input v-model="form.sku" placeholder="请输入SKU编码" />
        </el-form-item>
        
        <el-form-item label="产品分类" prop="category">
          <el-select v-model="form.category" placeholder="请选择产品分类" style="width: 100%">
            <el-option
              v-for="category in categories"
              :key="category.id"
              :label="category.name"
              :value="category.id"
            />
          </el-select>
        </el-form-item>
        
        <el-form-item label="供应商" prop="supplier">
          <el-select v-model="form.supplier" placeholder="请选择供应商" style="width: 100%">
            <el-option
              v-for="supplier in suppliers"
              :key="supplier.id"
              :label="supplier.name"
              :value="supplier.id"
            />
          </el-select>
        </el-form-item>
        
        <el-form-item label="单价" prop="unit_price">
          <el-input-number 
            v-model="form.unit_price" 
            :precision="2" 
            :step="0.01" 
            :min="0"
            style="width: 100%"
            placeholder="请输入单价"
          />
        </el-form-item>
        
        <el-form-item label="库存数量" prop="stock_quantity">
          <el-input-number 
            v-model="form.stock_quantity" 
            :min="0"
            style="width: 100%"
            placeholder="请输入库存数量"
          />
        </el-form-item>
        
        <el-form-item label="最低库存" prop="min_stock_level">
          <el-input-number 
            v-model="form.min_stock_level" 
            :min="0"
            style="width: 100%"
            placeholder="请输入最低库存水平"
          />
        </el-form-item>
        
        <el-form-item label="产品描述" prop="description">
          <el-input 
            v-model="form.description" 
            type="textarea" 
            :rows="4"
            placeholder="请输入产品描述" 
          />
        </el-form-item>
        
        <el-form-item>
          <el-button type="primary" @click="handleSubmit" :loading="loading">
            {{ isEdit ? '更新' : '创建' }}
          </el-button>
          <el-button @click="$router.go(-1)">取消</el-button>
        </el-form-item>
      </el-form>
    </div>
  </div>
</template>

<script>
import { ref, reactive, onMounted, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import api from '@/api'
import { ElMessage } from 'element-plus'

export default {
  name: 'ProductForm',
  setup() {
    const route = useRoute()
    const router = useRouter()
    const formRef = ref()
    const loading = ref(false)
    const categories = ref([])
    const suppliers = ref([])
    
    const isEdit = computed(() => route.params.id !== undefined)
    
    const form = reactive({
      name: '',
      sku: '',
      category: '',
      supplier: '',
      unit_price: 0,
      stock_quantity: 0,
      min_stock_level: 0,
      description: ''
    })
    
    const rules = {
      name: [
        { required: true, message: '请输入产品名称', trigger: 'blur' },
        { min: 2, max: 200, message: '长度在 2 到 200 个字符', trigger: 'blur' }
      ],
      sku: [
        { required: true, message: '请输入SKU编码', trigger: 'blur' },
        { min: 3, max: 50, message: '长度在 3 到 50 个字符', trigger: 'blur' }
      ],
      category: [
        { required: true, message: '请选择产品分类', trigger: 'change' }
      ],
      supplier: [
        { required: true, message: '请选择供应商', trigger: 'change' }
      ],
      unit_price: [
        { required: true, message: '请输入单价', trigger: 'blur' },
        { type: 'number', min: 0, message: '单价必须大于等于0', trigger: 'blur' }
      ],
      stock_quantity: [
        { required: true, message: '请输入库存数量', trigger: 'blur' },
        { type: 'number', min: 0, message: '库存数量必须大于等于0', trigger: 'blur' }
      ],
      min_stock_level: [
        { required: true, message: '请输入最低库存水平', trigger: 'blur' },
        { type: 'number', min: 0, message: '最低库存水平必须大于等于0', trigger: 'blur' }
      ]
    }
    
    const fetchCategories = async () => {
      try {
        const response = await api.get('/categories/')
        categories.value = response.data
      } catch (error) {
        ElMessage.error('获取产品分类失败')
      }
    }
    
    const fetchSuppliers = async () => {
      try {
        const response = await api.get('/suppliers/')
        suppliers.value = response.data
      } catch (error) {
        ElMessage.error('获取供应商列表失败')
      }
    }
    
    const fetchProduct = async (id) => {
      try {
        const response = await api.get(`/products/${id}/`)
        Object.assign(form, response.data)
      } catch (error) {
        ElMessage.error('获取产品信息失败')
        router.push('/products')
      }
    }
    
    const handleSubmit = async () => {
      if (!formRef.value) return
      
      try {
        await formRef.value.validate()
        loading.value = true
        
        if (isEdit.value) {
          await api.put(`/products/${route.params.id}/`, form)
          ElMessage.success('产品更新成功')
        } else {
          await api.post('/products/', form)
          ElMessage.success('产品创建成功')
        }
        
        router.push('/products')
      } catch (error) {
        if (error !== false) {
          ElMessage.error(isEdit.value ? '更新失败' : '创建失败')
        }
      } finally {
        loading.value = false
      }
    }
    
    onMounted(async () => {
      await Promise.all([fetchCategories(), fetchSuppliers()])
      if (isEdit.value) {
        fetchProduct(route.params.id)
      }
    })
    
    return {
      formRef,
      form,
      rules,
      loading,
      categories,
      suppliers,
      isEdit,
      handleSubmit
    }
  }
}
</script>

<style scoped>
.product-form {
  padding: 20px;
}

.form-container {
  background: #fff;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  padding: 30px;
  max-width: 600px;
  margin: 0 auto;
}

.form-title {
  font-size: 20px;
  font-weight: 600;
  color: #333;
  margin-bottom: 24px;
  text-align: center;
}
</style> 