#!/usr/bin/env python3
"""
YouTube视频下载器启动脚本
"""

import sys
import subprocess
import os
from pathlib import Path

def check_dependencies():
    """检查依赖是否安装"""
    try:
        import fastapi
        import uvicorn
        import yt_dlp
        import jinja2
        print("✓ 所有依赖已安装")
        return True
    except ImportError as e:
        print(f"✗ 缺少依赖: {e}")
        print("请运行以下命令安装依赖:")
        print("pip install -r requirements.txt")
        return False

def create_directories():
    """创建必要的目录"""
    dirs = ['downloads', 'templates', 'static']
    for dir_name in dirs:
        Path(dir_name).mkdir(exist_ok=True)
    print("✓ 目录结构检查完成")

def main():
    """主函数"""
    print("=" * 50)
    print("YouTube视频下载器启动脚本")
    print("=" * 50)
    
    # 检查依赖
    if not check_dependencies():
        sys.exit(1)
    
    # 创建目录
    create_directories()
    
    # 检查主文件是否存在
    if not Path('main.py').exists():
        print("✗ 找不到main.py文件")
        sys.exit(1)
    
    print("✓ 启动条件检查完成")
    print("\n正在启动服务器...")
    print("访问地址: http://localhost:8000")
    print("按 Ctrl+C 停止服务器\n")
    
    try:
        # 启动服务器
        os.system("python main.py")
    except KeyboardInterrupt:
        print("\n服务器已停止")
    except Exception as e:
        print(f"启动失败: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 