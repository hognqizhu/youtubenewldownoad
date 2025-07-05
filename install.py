#!/usr/bin/env python3
"""
YouTube视频下载器安装脚本
"""

import sys
import subprocess
import os
import stat
from pathlib import Path

def check_python_version():
    """检查Python版本"""
    if sys.version_info < (3, 8):
        print("✗ Python版本过低，需要Python 3.8+")
        print(f"当前版本: {sys.version}")
        return False
    print(f"✓ Python版本检查通过: {sys.version}")
    return True

def install_dependencies():
    """安装依赖"""
    print("正在安装依赖...")
    
    # 尝试不同的安装方法
    install_methods = [
        # 方法1: 使用 --user 标志
        ([sys.executable, '-m', 'pip', 'install', '--user', '-r', 'requirements.txt'], "使用 --user 标志安装"),
        # 方法2: 尝试创建虚拟环境
        (None, "创建虚拟环境"),
        # 方法3: 使用 --break-system-packages（不推荐）
        ([sys.executable, '-m', 'pip', 'install', '--break-system-packages', '-r', 'requirements.txt'], "使用 --break-system-packages 标志（不推荐）")
    ]
    
    for i, (cmd, description) in enumerate(install_methods, 1):
        print(f"尝试方法 {i}: {description}")
        
        if cmd is None:  # 虚拟环境方法
            try:
                # 创建虚拟环境
                venv_path = Path("venv")
                if not venv_path.exists():
                    print("创建虚拟环境...")
                    subprocess.check_call([sys.executable, '-m', 'venv', 'venv'])
                
                # 确定虚拟环境中的 Python 路径
                if sys.platform == "win32":
                    venv_python = venv_path / "Scripts" / "python.exe"
                    venv_pip = venv_path / "Scripts" / "pip.exe"
                else:
                    venv_python = venv_path / "bin" / "python"
                    venv_pip = venv_path / "bin" / "pip"
                
                # 升级 pip
                subprocess.check_call([str(venv_pip), 'install', '--upgrade', 'pip'])
                
                # 安装依赖
                subprocess.check_call([str(venv_pip), 'install', '-r', 'requirements.txt'])
                
                print("✓ 依赖安装成功（虚拟环境）")
                print(f"✓ 虚拟环境创建在: {venv_path.absolute()}")
                print("\n重要提示：")
                print("由于使用了虚拟环境，请使用以下命令启动应用:")
                if sys.platform == "win32":
                    print("  venv\\Scripts\\python.exe main.py")
                else:
                    print("  source venv/bin/activate")
                    print("  python main.py")
                print("或者直接运行: python run_with_venv.py")
                
                # 创建虚拟环境启动脚本
                create_venv_runner()
                return True
                
            except subprocess.CalledProcessError as e:
                print(f"✗ 虚拟环境安装失败: {e}")
                continue
        else:
            try:
                subprocess.check_call(cmd)
                print(f"✓ 依赖安装成功（{description}）")
                return True
            except subprocess.CalledProcessError as e:
                print(f"✗ 方法 {i} 失败: {e}")
                continue
    
    print("✗ 所有安装方法都失败了")
    print("\n手动安装建议:")
    print("1. 创建虚拟环境:")
    print("   python3 -m venv venv")
    print("   source venv/bin/activate  # macOS/Linux")
    print("   # 或者 venv\\Scripts\\activate  # Windows")
    print("2. 安装依赖:")
    print("   pip install -r requirements.txt")
    print("3. 运行应用:")
    print("   python main.py")
    
    return False

def create_venv_runner():
    """创建虚拟环境启动脚本"""
    if sys.platform == "win32":
        script_content = '''@echo off
echo 启动 YouTube 视频下载器（虚拟环境）
if not exist "venv" (
    echo 错误: 虚拟环境不存在
    pause
    exit /b 1
)
call venv\\Scripts\\activate.bat
python main.py
pause
'''
        with open("run_with_venv.bat", "w", encoding="utf-8") as f:
            f.write(script_content)
        print("✓ 创建了 run_with_venv.bat 启动脚本")
    else:
        script_content = '''#!/bin/bash
echo "启动 YouTube 视频下载器（虚拟环境）"
if [ ! -d "venv" ]; then
    echo "错误: 虚拟环境不存在"
    exit 1
fi
source venv/bin/activate
python main.py
'''
        with open("run_with_venv.sh", "w", encoding="utf-8") as f:
            f.write(script_content)
        
        # 添加执行权限
        script_path = Path("run_with_venv.sh")
        script_path.chmod(script_path.stat().st_mode | stat.S_IEXEC)
        print("✓ 创建了 run_with_venv.sh 启动脚本")
    
    # 创建 Python 启动脚本
    python_script = '''#!/usr/bin/env python3
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
        print("\\n应用已停止")
    except subprocess.CalledProcessError as e:
        print(f"运行失败: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
'''
    
    with open("run_with_venv.py", "w", encoding="utf-8") as f:
        f.write(python_script)
    print("✓ 创建了 run_with_venv.py 启动脚本")

def create_directories():
    """创建必要的目录"""
    dirs = ['downloads', 'static']
    for dir_name in dirs:
        Path(dir_name).mkdir(exist_ok=True)
        print(f"✓ 创建目录: {dir_name}")

def main():
    """主函数"""
    print("=" * 50)
    print("YouTube视频下载器安装脚本")
    print("=" * 50)
    
    # 检查Python版本
    if not check_python_version():
        sys.exit(1)
    
    # 检查requirements.txt是否存在
    if not Path('requirements.txt').exists():
        print("✗ 找不到requirements.txt文件")
        sys.exit(1)
    
    # 安装依赖
    if not install_dependencies():
        sys.exit(1)
    
    # 创建目录
    create_directories()
    
    print("\n" + "=" * 50)
    print("安装完成！")
    print("=" * 50)
    print("\n使用方法:")
    
    # 检查是否有虚拟环境
    if Path("venv").exists():
        print("✓ 检测到虚拟环境安装")
        print("推荐启动方式:")
        print("1. 运行: python run_with_venv.py")
        print("2. 或者手动激活虚拟环境:")
        if sys.platform == "win32":
            print("   venv\\Scripts\\activate")
        else:
            print("   source venv/bin/activate")
        print("   python main.py")
    else:
        print("✓ 检测到用户级别安装")
        print("启动方式:")
        print("1. 运行: python run.py")
        print("2. 或者运行: python main.py")
    
    print("\n3. 在浏览器中访问: http://localhost:8000")
    print("\n注意事项:")
    print("- 请确保网络连接正常")
    print("- 部分视频可能需要安装FFmpeg")
    print("- 仅下载您有权下载的内容")
    print("- 遵守YouTube服务条款，仅下载有权下载的内容")

if __name__ == "__main__":
    main() 