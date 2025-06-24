<template>
  <div class="supplier-form">
    <div class="form-container">
      <h2 class="form-title">{{ isEdit ? '编辑供应商' : '添加供应商' }}</h2>
      
      <el-form 
        ref="formRef" 
        :model="form" 
        :rules="rules" 
        label-width="120px"
        @submit.prevent="handleSubmit"
      >
        <el-form-item label="供应商名称" prop="name">
          <el-input v-model="form.name" placeholder="请输入供应商名称" />
        </el-form-item>
        
        <el-form-item label="联系人" prop="contact_person">
          <el-input v-model="form.contact_person" placeholder="请输入联系人姓名" />
        </el-form-item>
        
        <el-form-item label="联系电话" prop="phone">
          <el-input v-model="form.phone" placeholder="请输入联系电话" />
        </el-form-item>
        
        <el-form-item label="邮箱" prop="email">
          <el-input v-model="form.email" placeholder="请输入邮箱地址" />
        </el-form-item>
        
        <el-form-item label="地址" prop="address">
          <el-input 
            v-model="form.address" 
            type="textarea" 
            :rows="3"
            placeholder="请输入详细地址" 
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
  name: 'SupplierForm',
  setup() {
    const route = useRoute()
    const router = useRouter()
    const formRef = ref()
    const loading = ref(false)
    
    const isEdit = computed(() => route.params.id !== undefined)
    
    const form = reactive({
      name: '',
      contact_person: '',
      phone: '',
      email: '',
      address: ''
    })
    
    const rules = {
      name: [
        { required: true, message: '请输入供应商名称', trigger: 'blur' },
        { min: 2, max: 200, message: '长度在 2 到 200 个字符', trigger: 'blur' }
      ],
      contact_person: [
        { required: true, message: '请输入联系人姓名', trigger: 'blur' }
      ],
      phone: [
        { required: true, message: '请输入联系电话', trigger: 'blur' },
        { pattern: /^1[3-9]\d{9}$/, message: '请输入正确的手机号码', trigger: 'blur' }
      ],
      email: [
        { required: true, message: '请输入邮箱地址', trigger: 'blur' },
        { type: 'email', message: '请输入正确的邮箱地址', trigger: 'blur' }
      ],
      address: [
        { required: true, message: '请输入地址', trigger: 'blur' }
      ]
    }
    
    const fetchSupplier = async (id) => {
      try {
        const response = await api.get(`/suppliers/${id}/`)
        Object.assign(form, response.data)
      } catch (error) {
        ElMessage.error('获取供应商信息失败')
        router.push('/suppliers')
      }
    }
    
    const handleSubmit = async () => {
      if (!formRef.value) return
      
      try {
        await formRef.value.validate()
        loading.value = true
        
        if (isEdit.value) {
          await api.put(`/suppliers/${route.params.id}/`, form)
          ElMessage.success('供应商更新成功')
        } else {
          await api.post('/suppliers/', form)
          ElMessage.success('供应商创建成功')
        }
        
        router.push('/suppliers')
      } catch (error) {
        if (error !== false) {
          ElMessage.error(isEdit.value ? '更新失败' : '创建失败')
        }
      } finally {
        loading.value = false
      }
    }
    
    onMounted(() => {
      if (isEdit.value) {
        fetchSupplier(route.params.id)
      }
    })
    
    return {
      formRef,
      form,
      rules,
      loading,
      isEdit,
      handleSubmit
    }
  }
}
</script>

<style scoped>
.supplier-form {
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