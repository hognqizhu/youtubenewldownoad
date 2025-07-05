# YouTube视频下载器

一个基于FastAPI和yt-dlp的简单而强大的YouTube视频下载站点。

## 功能特点

- 🎬 **视频下载**: 输入YouTube链接即可下载视频
- 📊 **实时进度**: 下载过程中显示实时进度条
- 🎥 **在线预览**: 使用HTML5播放器直接预览下载的视频
- 📁 **视频管理**: 查看已下载视频列表，包含详细信息
- 🗑️ **删除功能**: 一键删除不需要的视频文件
- 🎨 **美观界面**: 使用TailwindCSS设计的现代化界面
- 📱 **响应式设计**: 支持手机和平板等各种设备

## 技术栈

- **后端**: FastAPI + Python
- **前端**: HTML5 + JavaScript + TailwindCSS
- **模板引擎**: Jinja2
- **视频下载**: yt-dlp
- **服务器**: Uvicorn

## 快速开始

### 方法一：使用安装脚本（推荐）
```bash
# 1. 下载或克隆项目
git clone <your-repo-url>
cd YoutubeNewdownload

# 2. 运行安装脚本（自动处理环境问题）
python install.py

# 3. 启动应用（根据安装结果选择）
# 如果使用虚拟环境安装：
python run_with_venv.py
# 如果使用 --user 标志安装：
python run.py
```

### 方法二：手动安装
```bash
# 1. 克隆项目
git clone <your-repo-url>
cd YoutubeNewdownload

# 2. 安装依赖
pip install -r requirements.txt

# 3. 运行应用
python main.py
```

### 方法三：使用uvicorn直接运行
```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

### 访问应用
在浏览器中打开 `http://localhost:8000`

### 测试功能
```bash
# 运行演示脚本
python demo.py
```

## 使用方法

1. **下载视频**
   - 在主页输入YouTube视频链接
   - 点击"开始下载"按钮
   - 等待下载完成

2. **查看视频**
   - 下载完成后，视频会自动显示在页面下方
   - 点击视频播放器即可预览视频

3. **管理视频**
   - 在视频列表中可以看到所有已下载的视频
   - 每个视频显示标题、作者、时长、大小等信息
   - 点击"删除"按钮可以删除不需要的视频

## 项目结构

```
YoutubeNewdownload/
├── main.py                 # 主应用文件
├── requirements.txt        # 依赖文件
├── README.md              # 项目说明
├── templates/             # 模板目录
│   └── index.html         # 主页模板
├── downloads/             # 下载目录（自动创建）
│   ├── videos_info.json   # 视频信息存储
│   └── *.mp4              # 下载的视频文件
└── static/                # 静态文件目录（可选）
```

## API接口

### 主要端点

- `GET /` - 主页
- `POST /download` - 下载视频
- `GET /status/{video_id}` - 获取下载状态
- `GET /videos` - 获取已下载视频列表
- `DELETE /videos/{filename}` - 删除视频

### 下载接口示例

```bash
curl -X POST "http://localhost:8000/download" \
     -H "Content-Type: application/json" \
     -d '{"url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ"}'
```

## 配置选项

在 `main.py` 中可以修改以下配置：

- `DOWNLOAD_DIR`: 下载目录路径
- `ydl_opts`: yt-dlp下载选项
- 服务器端口和主机地址

## 注意事项

1. **合法使用**: 请确保遵守YouTube的服务条款，仅下载您有权下载的内容
2. **网络连接**: 下载需要稳定的网络连接
3. **存储空间**: 确保有足够的磁盘空间存储视频文件
4. **FFmpeg**: 某些视频格式可能需要安装FFmpeg

## 故障排除

### 常见问题

1. **Python环境管理问题（macOS/Linux）**
   ```
   error: externally-managed-environment
   ```
   **解决方案：**
   - 运行 `python install.py` 脚本会自动处理这个问题
   - 或者手动创建虚拟环境：
     ```bash
     python3 -m venv venv
     source venv/bin/activate
     pip install -r requirements.txt
     ```

2. **依赖安装失败**
   - 确保Python版本 >= 3.8
   - 尝试升级pip: `pip install --upgrade pip`
   - 如果使用虚拟环境：`venv/bin/pip install --upgrade pip`

3. **下载失败**
   - 检查网络连接
   - 验证YouTube链接是否有效
   - 检查视频是否有地区限制

4. **视频无法播放**
   - 确保浏览器支持HTML5视频
   - 检查视频文件是否完整下载

5. **虚拟环境相关**
   - 如果提示找不到 `run_with_venv.py`，重新运行 `python install.py`
   - 删除 `venv` 目录后重新安装：`rm -rf venv && python install.py`

### 日志查看

应用运行时会在控制台输出详细日志，包括：
- 下载进度
- 错误信息
- 文件处理状态

## 开发相关

### 本地开发

```bash
# 开发模式运行
uvicorn main:app --reload

# 查看API文档
# 访问 http://localhost:8000/docs
```

### 自定义扩展

你可以根据需要修改以下部分：
- UI界面样式
- 下载质量设置
- 文件命名规则
- 支持的视频平台

## 许可证

MIT License

## 贡献

欢迎提交Issue和Pull Request来改进这个项目！

## 更新日志

- v1.0.0: 初始版本发布
  - 基本下载功能
  - 视频管理
  - 现代化界面 