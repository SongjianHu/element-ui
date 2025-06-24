<template>
  <div id="app">
    <el-container class="app-container">
      <el-aside width="250px" class="sidebar">
        <div class="logo">
          <h2>供应链管理系统</h2>
        </div>
        <el-menu
          :default-active="$route.path"
          class="sidebar-menu"
          router
          background-color="#304156"
          text-color="#bfcbd9"
          active-text-color="#409EFF"
        >
          <el-menu-item index="/dashboard">
            <el-icon><DataBoard /></el-icon>
            <span>仪表板</span>
          </el-menu-item>
          
          <el-sub-menu index="suppliers">
            <template #title>
              <el-icon><Shop /></el-icon>
              <span>供应商管理</span>
            </template>
            <el-menu-item index="/suppliers">供应商列表</el-menu-item>
            <el-menu-item index="/suppliers/add">添加供应商</el-menu-item>
          </el-sub-menu>
          
          <el-sub-menu index="products">
            <template #title>
              <el-icon><Goods /></el-icon>
              <span>产品管理</span>
            </template>
            <el-menu-item index="/products">产品列表</el-menu-item>
            <el-menu-item index="/products/add">添加产品</el-menu-item>
            <el-menu-item index="/categories">产品分类</el-menu-item>
          </el-sub-menu>
          
          <el-sub-menu index="orders">
            <template #title>
              <el-icon><Document /></el-icon>
              <span>采购订单</span>
            </template>
            <el-menu-item index="/purchase-orders">订单列表</el-menu-item>
            <el-menu-item index="/purchase-orders/add">创建订单</el-menu-item>
          </el-sub-menu>
          
          <el-sub-menu index="inventory">
            <template #title>
              <el-icon><Box /></el-icon>
              <span>库存管理</span>
            </template>
            <el-menu-item index="/inventory">库存概览</el-menu-item>
            <el-menu-item index="/inventory/low-stock">库存预警</el-menu-item>
          </el-sub-menu>
        </el-menu>
      </el-aside>
      
      <el-container>
        <el-header class="header">
          <div class="header-left">
            <el-breadcrumb separator="/">
              <el-breadcrumb-item v-for="item in breadcrumbs" :key="item.path" :to="item.path">
                {{ item.name }}
              </el-breadcrumb-item>
            </el-breadcrumb>
          </div>
          <div class="header-right">
            <el-dropdown>
              <span class="user-info">
                <el-avatar size="small" icon="UserFilled" />
                <span class="username">管理员</span>
              </span>
              <template #dropdown>
                <el-dropdown-menu>
                  <el-dropdown-item>个人设置</el-dropdown-item>
                  <el-dropdown-item divided>退出登录</el-dropdown-item>
                </el-dropdown-menu>
              </template>
            </el-dropdown>
          </div>
        </el-header>
        
        <el-main class="main-content">
          <router-view />
        </el-main>
      </el-container>
    </el-container>
  </div>
</template>

<script>
import { ref, computed } from 'vue'
import { useRoute } from 'vue-router'

export default {
  name: 'App',
  setup() {
    const route = useRoute()
    
    const breadcrumbs = computed(() => {
      const paths = route.path.split('/').filter(Boolean)
      const breadcrumbItems = [{ path: '/', name: '首页' }]
      
      paths.forEach((path, index) => {
        const fullPath = '/' + paths.slice(0, index + 1).join('/')
        const name = getBreadcrumbName(path)
        breadcrumbItems.push({ path: fullPath, name })
      })
      
      return breadcrumbItems
    })
    
    const getBreadcrumbName = (path) => {
      const nameMap = {
        'dashboard': '仪表板',
        'suppliers': '供应商管理',
        'products': '产品管理',
        'categories': '产品分类',
        'purchase-orders': '采购订单',
        'inventory': '库存管理',
        'add': '添加',
        'low-stock': '库存预警'
      }
      return nameMap[path] || path
    }
    
    return {
      breadcrumbs
    }
  }
}
</script>

<style scoped>
.app-container {
  height: 100vh;
}

.sidebar {
  background-color: #304156;
  color: #bfcbd9;
}

.logo {
  padding: 20px;
  text-align: center;
  border-bottom: 1px solid #435266;
}

.logo h2 {
  color: #fff;
  margin: 0;
  font-size: 18px;
}

.sidebar-menu {
  border-right: none;
}

.header {
  background-color: #fff;
  border-bottom: 1px solid #e6e6e6;
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 20px;
}

.header-left {
  flex: 1;
}

.header-right {
  display: flex;
  align-items: center;
}

.user-info {
  display: flex;
  align-items: center;
  cursor: pointer;
  padding: 8px 12px;
  border-radius: 4px;
  transition: background-color 0.3s;
}

.user-info:hover {
  background-color: #f5f5f5;
}

.username {
  margin-left: 8px;
  color: #333;
}

.main-content {
  background-color: #f0f2f5;
  padding: 20px;
}
</style> 