#!/usr/bin/env python3
"""
YouTube视频下载器演示脚本
"""

import sys
import time
import requests
import json
from pathlib import Path

def test_api():
    """测试API接口"""
    base_url = "http://localhost:8000"
    
    print("正在测试API接口...")
    
    # 测试主页
    try:
        response = requests.get(base_url)
        if response.status_code == 200:
            print("✓ 主页访问正常")
        else:
            print(f"✗ 主页访问失败: {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("✗ 无法连接到服务器，请确保服务器正在运行")
        return False
    
    # 测试视频列表接口
    try:
        response = requests.get(f"{base_url}/videos")
        if response.status_code == 200:
            videos = response.json()
            print(f"✓ 视频列表接口正常，当前有 {len(videos)} 个视频")
        else:
            print(f"✗ 视频列表接口失败: {response.status_code}")
    except Exception as e:
        print(f"✗ 视频列表接口错误: {e}")
    
    return True

def demo_download():
    """演示下载功能"""
    print("\n" + "=" * 50)
    print("YouTube视频下载器演示")
    print("=" * 50)
    
    # 示例视频URL（Rick Roll - 经典测试视频）
    test_urls = [
        "https://www.youtube.com/watch?v=dQw4w9WgXcQ",  # Rick Roll
        "https://www.youtube.com/watch?v=9bZkp7q19f0",  # Gangnam Style
    ]
    
    print("\n可用于测试的视频URL:")
    for i, url in enumerate(test_urls, 1):
        print(f"{i}. {url}")
    
    print("\n请手动在浏览器中测试以下功能:")
    print("1. 打开浏览器，访问 http://localhost:8000")
    print("2. 复制上述任一URL到输入框")
    print("3. 点击'开始下载'按钮")
    print("4. 观察下载进度")
    print("5. 下载完成后查看视频列表")
    print("6. 尝试播放下载的视频")
    print("7. 测试删除视频功能")
    
    print("\n注意事项:")
    print("- 首次下载可能需要较长时间")
    print("- 请确保网络连接稳定")
    print("- 某些视频可能受地区限制")

def check_project_structure():
    """检查项目结构"""
    print("检查项目结构...")
    
    required_files = [
        "main.py",
        "requirements.txt",
        "templates/index.html",
        "README.md"
    ]
    
    missing_files = []
    for file_path in required_files:
        if not Path(file_path).exists():
            missing_files.append(file_path)
        else:
            print(f"✓ {file_path}")
    
    if missing_files:
        print(f"\n✗ 缺少以下文件:")
        for file_path in missing_files:
            print(f"  - {file_path}")
        return False
    
    print("✓ 项目结构完整")
    return True

def main():
    """主函数"""
    print("=" * 50)
    print("YouTube视频下载器演示脚本")
    print("=" * 50)
    
    # 检查项目结构
    if not check_project_structure():
        print("\n请确保所有必需文件都存在")
        sys.exit(1)
    
    # 测试API（如果服务器正在运行）
    if test_api():
        demo_download()
    else:
        print("\n服务器未运行，请先启动服务器:")
        print("1. 运行: python install.py (首次使用)")
        print("2. 运行: python run.py")
        print("3. 然后再次运行此演示脚本")

if __name__ == "__main__":
    main() 