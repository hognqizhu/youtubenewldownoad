#!/bin/bash
echo "启动 YouTube 视频下载器（虚拟环境）"
if [ ! -d "venv" ]; then
    echo "错误: 虚拟环境不存在"
    exit 1
fi
source venv/bin/activate
python main.py
