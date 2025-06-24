@echo off
echo 启动供应链管理系统后端...

cd backend

echo 检查Python虚拟环境...
if not exist "venv" (
    echo 创建虚拟环境...
    python -m venv venv
)

echo 激活虚拟环境...
call venv\Scripts\activate

echo 安装依赖...
pip install -r ..\requirements.txt

echo 执行数据库迁移...
python manage.py makemigrations
python manage.py migrate

echo 启动Django开发服务器...
python manage.py runserver

pause 