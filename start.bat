@echo off
echo 正在启动智能食谱助手...
echo.

echo 1. 启动后端服务...
start cmd /k "cd backend-flask && python app.py"
echo.

echo 2. 等待5秒后启动前端...
timeout /t 5 /nobreak

echo 3. 启动前端服务...
start cmd /k "cd frontend-react && npm start"
echo.

echo 4. 正在打开浏览器...
timeout /t 3 /nobreak
start http://localhost:3000

echo.
echo 智能食谱助手启动完成!
echo 如需关闭，请关闭相应的命令行窗口
echo. 