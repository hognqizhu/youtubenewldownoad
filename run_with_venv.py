#!/usr/bin/env python3
"""
虚拟环境启动脚本
"""
import sys
import subprocess
from pathlib import Path

def main():
    print("启动 YouTube 视频下载器（虚拟环境）")
    
    venv_path = Path("venv")
    if not venv_path.exists():
        print("错误: 虚拟环境不存在")
        print("请先运行: python install.py")
        sys.exit(1)
    
    # 确定虚拟环境中的 Python 路径
    if sys.platform == "win32":
        venv_python = venv_path / "Scripts" / "python.exe"
    else:
        venv_python = venv_path / "bin" / "python"
    
    if not venv_python.exists():
        print("错误: 虚拟环境损坏")
        sys.exit(1)
    
    # 运行主应用
    try:
        subprocess.check_call([str(venv_python), "main.py"])
    except KeyboardInterrupt:
        print("\n应用已停止")
    except subprocess.CalledProcessError as e:
        print(f"运行失败: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
