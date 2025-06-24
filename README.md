# 供应链管理系统

这是一个基于Vue.js + Element Plus前端和Django后端的供应链管理系统。

## 功能特性

- 🏢 **供应商管理** - 管理供应商信息，包括联系人、联系方式等
- 📦 **产品管理** - 管理产品信息，包括分类、SKU、价格等
- 📋 **采购订单** - 创建和管理采购订单，支持订单状态跟踪
- 📊 **库存管理** - 实时库存监控，库存预警功能
- 📈 **数据仪表板** - 可视化数据展示，包括订单统计、库存状态等

## 技术栈

### 后端
- Django 4.2.7
- Django REST Framework 3.14.0
- Django CORS Headers 4.3.1
- JWT认证

### 前端
- Vue.js 3.3.4
- Element Plus 2.4.2
- Vue Router 4.2.5
- Vuex 4.1.0
- Axios 1.6.0

## 项目结构

```
SupplyChain/
├── backend/                 # Django后端
│   ├── manage.py
│   ├── supply_chain/       # Django项目配置
│   └── supply_chain_api/   # 供应链API应用
├── frontend/               # Vue.js前端
│   ├── public/
│   ├── src/
│   │   ├── views/         # 页面组件
│   │   ├── components/    # 通用组件
│   │   ├── router/        # 路由配置
│   │   ├── store/         # 状态管理
│   │   ├── api/           # API请求
│   │   └── styles/        # 样式文件
│   └── package.json
├── requirements.txt        # Python依赖
└── README.md
```

## 安装和运行

### 1. 克隆项目

```bash
git clone <repository-url>
cd SupplyChain
```

### 2. 后端设置

```bash
# 创建虚拟环境
python -m venv venv

# 激活虚拟环境
# Windows
venv\Scripts\activate
# macOS/Linux
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt

# 进入后端目录
cd backend

# 数据库迁移
python manage.py makemigrations
python manage.py migrate

# 创建超级用户
python manage.py createsuperuser

# 运行开发服务器
python manage.py runserver
```

### 3. 前端设置

```bash
# 进入前端目录
cd frontend

# 安装依赖
npm install

# 运行开发服务器
npm run serve
```

## 访问地址

- 前端应用: http://localhost:8080
- 后端API: http://localhost:8000/api/
- Django管理后台: http://localhost:8000/admin/

## API接口

### 供应商管理
- `GET /api/suppliers/` - 获取供应商列表
- `POST /api/suppliers/` - 创建供应商
- `GET /api/suppliers/{id}/` - 获取供应商详情
- `PUT /api/suppliers/{id}/` - 更新供应商
- `DELETE /api/suppliers/{id}/` - 删除供应商

### 产品管理
- `GET /api/products/` - 获取产品列表
- `POST /api/products/` - 创建产品
- `GET /api/products/{id}/` - 获取产品详情
- `PUT /api/products/{id}/` - 更新产品
- `DELETE /api/products/{id}/` - 删除产品
- `GET /api/products/low_stock/` - 获取库存不足产品

### 采购订单
- `GET /api/purchase-orders/` - 获取订单列表
- `POST /api/purchase-orders/` - 创建订单
- `GET /api/purchase-orders/{id}/` - 获取订单详情
- `PUT /api/purchase-orders/{id}/` - 更新订单
- `POST /api/purchase-orders/{id}/approve/` - 批准订单
- `POST /api/purchase-orders/{id}/ship/` - 标记发货
- `POST /api/purchase-orders/{id}/receive/` - 标记收货
- `GET /api/purchase-orders/dashboard/` - 获取订单仪表板数据

### 库存管理
- `GET /api/inventory/` - 获取库存列表
- `GET /api/inventory/low_stock/` - 获取库存预警
- `GET /api/inventory/dashboard/` - 获取库存仪表板数据

## 主要功能模块

### 1. 仪表板
- 订单统计概览
- 库存状态监控
- 最近订单列表
- 库存预警提醒

### 2. 供应商管理
- 供应商信息维护
- 联系人管理
- 供应商搜索和筛选

### 3. 产品管理
- 产品信息维护
- 产品分类管理
- SKU编码管理
- 价格和库存设置

### 4. 采购订单
- 订单创建和编辑
- 订单状态跟踪
- 订单审批流程
- 收货确认

### 5. 库存管理
- 实时库存监控
- 库存预警
- 库存价值统计

## 开发说明

### 数据库模型

系统包含以下主要数据模型：

- **Supplier** - 供应商信息
- **Category** - 产品分类
- **Product** - 产品信息
- **PurchaseOrder** - 采购订单
- **PurchaseOrderItem** - 订单项目
- **Inventory** - 库存信息

### 前端组件

主要页面组件：

- `Dashboard.vue` - 仪表板页面
- `SupplierList.vue` - 供应商列表
- `SupplierForm.vue` - 供应商表单
- `ProductList.vue` - 产品列表
- `ProductForm.vue` - 产品表单
- `PurchaseOrderList.vue` - 订单列表
- `PurchaseOrderForm.vue` - 订单表单
- `InventoryList.vue` - 库存列表

## 部署说明

### 生产环境部署

1. **后端部署**
   - 使用Gunicorn作为WSGI服务器
   - 配置Nginx作为反向代理
   - 使用PostgreSQL作为生产数据库

2. **前端部署**
   - 构建生产版本：`npm run build`
   - 将dist目录部署到Web服务器

## 贡献指南

1. Fork项目
2. 创建功能分支
3. 提交更改
4. 推送到分支
5. 创建Pull Request

## 许可证

MIT License

## 联系方式

如有问题或建议，请提交Issue或联系开发团队。 