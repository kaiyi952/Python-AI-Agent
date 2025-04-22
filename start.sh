#!/bin/bash

echo "正在启动智能食谱助手..."
echo

echo "1. 启动后端服务..."
cd backend-flask && python app.py &
BACKEND_PID=$!
echo "后端服务已启动，PID: $BACKEND_PID"
echo

echo "2. 等待5秒后启动前端..."
sleep 5

echo "3. 启动前端服务..."
cd ../frontend-react && npm start &
FRONTEND_PID=$!
echo "前端服务已启动，PID: $FRONTEND_PID"
echo

echo "4. 正在打开浏览器..."
sleep 3
if [[ "$OSTYPE" == "darwin"* ]]; then
  open http://localhost:3000
elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
  xdg-open http://localhost:3000
fi

echo
echo "智能食谱助手启动完成!"
echo "按Ctrl+C关闭所有服务"

# 等待用户按Ctrl+C
trap "kill $BACKEND_PID $FRONTEND_PID; exit" INT
wait 