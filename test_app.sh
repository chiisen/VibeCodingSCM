#!/bin/bash
echo "SCM 供应链管理系统启动测试"
echo "=========================="

# 检查 Python 是否安装
echo "1. 检查 Python 版本..."
python --version

# 检查 Flask 是否安装
echo "2. 检查 Flask 是否安装..."
python -c "import flask; print('Flask 版本:', flask.__version__)"

# 启动应用（后台运行）
echo "3. 启动 Flask 应用..."
python app.py &
APP_PID=$!

# 等待几秒让应用启动
echo "等待应用启动..."
sleep 5

# 测试应用是否响应
echo "4. 测试应用响应..."
curl -s http://localhost:5000 | head -20

# 停止应用
echo "5. 停止应用..."
kill $APP_PID

echo "测试完成！"
