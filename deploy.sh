#!/bin/bash

# 停止旧服务（如果存在）
pid=$(ps -ef | grep "uvicorn app.main:app" | grep -v grep | awk '{print $2}')
if [ ! -z "$pid" ]; then
    kill -9 $pid
fi

# 启动服务
nohup /usr/local/bin/python3 -m uvicorn app.main:app --host 0.0.0.0 --port 8600 > app.log 2>&1 &

echo "Service deployed successfully!"

# 显示运行状态
sleep 2
ps -ef | grep uvicorn | grep -v grep
echo "Check logs with: tail -f app.log"