@echo off
echo 启动供应链管理系统前端...

cd frontend

echo 安装依赖...
npm install

echo 启动Vue开发服务器...
npm run serve

pause 