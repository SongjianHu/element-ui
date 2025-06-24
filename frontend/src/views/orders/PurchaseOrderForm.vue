<template>
  <div class="purchase-order-form">
    <div class="form-container">
      <h2 class="form-title">{{ isEdit ? '编辑采购订单' : '创建采购订单' }}</h2>
      
      <el-form 
        ref="formRef" 
        :model="form" 
        :rules="rules" 
        label-width="120px"
        @submit.prevent="handleSubmit"
      >
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
        
        <el-form-item label="订单日期" prop="order_date">
          <el-date-picker
            v-model="form.order_date"
            type="date"
            placeholder="选择订单日期"
            style="width: 100%"
            format="YYYY-MM-DD"
            value-format="YYYY-MM-DD"
          />
        </el-form-item>
        
        <el-form-item label="预计交货日期" prop="expected_delivery_date">
          <el-date-picker
            v-model="form.expected_delivery_date"
            type="date"
            placeholder="选择预计交货日期"
            style="width: 100%"
            format="YYYY-MM-DD"
            value-format="YYYY-MM-DD"
          />
        </el-form-item>
        
        <el-form-item label="备注" prop="notes">
          <el-input 
            v-model="form.notes" 
            type="textarea" 
            :rows="3"
            placeholder="请输入订单备注" 
          />
        </el-form-item>
        
        <!-- 订单项目 -->
        <el-form-item label="订单项目">
          <div class="order-items">
            <div class="item-header">
              <h4>订单项目</h4>
              <el-button type="primary" size="small" @click="addItem">
                <el-icon><Plus /></el-icon>
                添加项目
              </el-button>
            </div>
            
            <div v-for="(item, index) in form.items" :key="index" class="order-item">
              <el-row :gutter="16">
                <el-col :span="8">
                  <el-form-item :label="'产品' + (index + 1)" :prop="`items.${index}.product`">
                    <el-select 
                      v-model="item.product" 
                      placeholder="选择产品"
                      style="width: 100%"
                      @change="onProductChange(index)"
                    >
                      <el-option
                        v-for="product in products"
                        :key="product.id"
                        :label="`${product.name} (${product.sku})`"
                        :value="product.id"
                      />
                    </el-select>
                  </el-form-item>
                </el-col>
                <el-col :span="4">
                  <el-form-item label="数量" :prop="`items.${index}.quantity`">
                    <el-input-number 
                      v-model="item.quantity" 
                      :min="1"
                      style="width: 100%"
                      @change="calculateItemTotal(index)"
                    />
                  </el-form-item>
                </el-col>
                <el-col :span="4">
                  <el-form-item label="单价" :prop="`items.${index}.unit_price`">
                    <el-input-number 
                      v-model="item.unit_price" 
                      :precision="2"
                      :step="0.01"
                      :min="0"
                      style="width: 100%"
                      @change="calculateItemTotal(index)"
                    />
                  </el-form-item>
                </el-col>
                <el-col :span="4">
                  <el-form-item label="总价">
                    <el-input 
                      v-model="item.total_price" 
                      readonly
                      style="width: 100%"
                    />
                  </el-form-item>
                </el-col>
                <el-col :span="4">
                  <el-button 
                    type="danger" 
                    size="small" 
                    @click="removeItem(index)"
                    :disabled="form.items.length === 1"
                  >
                    删除
                  </el-button>
                </el-col>
              </el-row>
            </div>
          </div>
        </el-form-item>
        
        <el-form-item label="订单总金额">
          <el-input 
            v-model="form.total_amount" 
            readonly
            style="width: 200px"
          >
            <template #prepend>¥</template>
          </el-input>
        </el-form-item>
        
        <el-form-item>
          <el-button type="primary" @click="handleSubmit" :loading="loading">
            {{ isEdit ? '更新订单' : '创建订单' }}
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
  name: 'PurchaseOrderForm',
  setup() {
    const route = useRoute()
    const router = useRouter()
    const formRef = ref()
    const loading = ref(false)
    const suppliers = ref([])
    const products = ref([])
    
    const isEdit = computed(() => route.params.id !== undefined)
    
    const form = reactive({
      supplier: '',
      order_date: '',
      expected_delivery_date: '',
      notes: '',
      items: [
        {
          product: '',
          quantity: 1,
          unit_price: 0,
          total_price: 0
        }
      ],
      total_amount: 0
    })
    
    const rules = {
      supplier: [
        { required: true, message: '请选择供应商', trigger: 'change' }
      ],
      order_date: [
        { required: true, message: '请选择订单日期', trigger: 'change' }
      ],
      expected_delivery_date: [
        { required: true, message: '请选择预计交货日期', trigger: 'change' }
      ]
    }
    
    const fetchSuppliers = async () => {
      try {
        const response = await api.get('/suppliers/')
        suppliers.value = response.data
      } catch (error) {
        ElMessage.error('获取供应商列表失败')
      }
    }
    
    const fetchProducts = async () => {
      try {
        const response = await api.get('/products/')
        products.value = response.data
      } catch (error) {
        ElMessage.error('获取产品列表失败')
      }
    }
    
    const fetchOrder = async (id) => {
      try {
        const response = await api.get(`/purchase-orders/${id}/`)
        Object.assign(form, response.data)
        // 处理订单项目
        if (response.data.items) {
          form.items = response.data.items.map(item => ({
            product: item.product,
            quantity: item.quantity,
            unit_price: item.unit_price,
            total_price: item.total_price
          }))
        }
        calculateTotal()
      } catch (error) {
        ElMessage.error('获取订单信息失败')
        router.push('/purchase-orders')
      }
    }
    
    const addItem = () => {
      form.items.push({
        product: '',
        quantity: 1,
        unit_price: 0,
        total_price: 0
      })
    }
    
    const removeItem = (index) => {
      form.items.splice(index, 1)
      calculateTotal()
    }
    
    const onProductChange = (index) => {
      const product = products.value.find(p => p.id === form.items[index].product)
      if (product) {
        form.items[index].unit_price = product.unit_price
        calculateItemTotal(index)
      }
    }
    
    const calculateItemTotal = (index) => {
      const item = form.items[index]
      item.total_price = item.quantity * item.unit_price
      calculateTotal()
    }
    
    const calculateTotal = () => {
      form.total_amount = form.items.reduce((total, item) => {
        return total + (item.total_price || 0)
      }, 0)
    }
    
    const handleSubmit = async () => {
      if (!formRef.value) return
      
      try {
        await formRef.value.validate()
        loading.value = true
        
        const orderData = {
          ...form,
          items: form.items.map(item => ({
            product: item.product,
            quantity: item.quantity,
            unit_price: item.unit_price
          }))
        }
        
        if (isEdit.value) {
          await api.put(`/purchase-orders/${route.params.id}/`, orderData)
          ElMessage.success('订单更新成功')
        } else {
          await api.post('/purchase-orders/', orderData)
          ElMessage.success('订单创建成功')
        }
        
        router.push('/purchase-orders')
      } catch (error) {
        if (error !== false) {
          ElMessage.error(isEdit.value ? '更新失败' : '创建失败')
        }
      } finally {
        loading.value = false
      }
    }
    
    onMounted(async () => {
      await Promise.all([fetchSuppliers(), fetchProducts()])
      if (isEdit.value) {
        fetchOrder(route.params.id)
      }
    })
    
    return {
      formRef,
      form,
      rules,
      loading,
      suppliers,
      products,
      isEdit,
      addItem,
      removeItem,
      onProductChange,
      calculateItemTotal,
      handleSubmit
    }
  }
}
</script>

<style scoped>
.purchase-order-form {
  padding: 20px;
}

.form-container {
  background: #fff;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  padding: 30px;
  max-width: 1000px;
  margin: 0 auto;
}

.form-title {
  font-size: 20px;
  font-weight: 600;
  color: #333;
  margin-bottom: 24px;
  text-align: center;
}

.order-items {
  border: 1px solid #e4e7ed;
  border-radius: 4px;
  padding: 16px;
}

.item-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16px;
}

.item-header h4 {
  margin: 0;
  color: #333;
}

.order-item {
  border: 1px solid #f0f0f0;
  border-radius: 4px;
  padding: 16px;
  margin-bottom: 16px;
  background-color: #fafafa;
}

.order-item:last-child {
  margin-bottom: 0;
}
</style> 