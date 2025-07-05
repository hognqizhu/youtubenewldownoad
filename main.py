import os
import json
import asyncio
from pathlib import Path
from typing import List, Dict, Optional
from datetime import datetime
import logging

from fastapi import FastAPI, Request, HTTPException, BackgroundTasks
from fastapi.responses import HTMLResponse, JSONResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
import yt_dlp
import uvicorn

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 创建FastAPI应用
app = FastAPI(title="YouTube视频下载器", version="1.0.0")

# 配置模板目录
templates = Jinja2Templates(directory="templates")

# 创建下载目录
DOWNLOAD_DIR = Path("downloads")
DOWNLOAD_DIR.mkdir(exist_ok=True)

# 静态文件目录
STATIC_DIR = Path("static")
STATIC_DIR.mkdir(exist_ok=True)

# 如果静态文件目录存在，则挂载
if STATIC_DIR.exists():
    app.mount("/static", StaticFiles(directory="static"), name="static")

# 挂载下载目录作为静态文件
app.mount("/downloads", StaticFiles(directory="downloads"), name="downloads")

# 请求模型
class VideoURL(BaseModel):
    url: str

class VideoInfo(BaseModel):
    title: str
    duration: Optional[int] = None
    uploader: Optional[str] = None
    description: Optional[str] = None
    file_size: Optional[int] = None
    file_path: str
    downloaded_at: str

# 全局变量存储下载状态
download_status = {}
downloaded_videos = []

# 加载已下载的视频信息
def load_downloaded_videos():
    global downloaded_videos
    info_file = DOWNLOAD_DIR / "videos_info.json"
    if info_file.exists():
        try:
            with open(info_file, 'r', encoding='utf-8') as f:
                downloaded_videos = json.load(f)
        except Exception as e:
            logger.error(f"加载视频信息失败: {e}")
            downloaded_videos = []
    else:
        downloaded_videos = []

# 保存视频信息
def save_video_info(video_info: VideoInfo):
    global downloaded_videos
    downloaded_videos.append(video_info.dict())
    info_file = DOWNLOAD_DIR / "videos_info.json"
    try:
        with open(info_file, 'w', encoding='utf-8') as f:
            json.dump(downloaded_videos, f, ensure_ascii=False, indent=2)
    except Exception as e:
        logger.error(f"保存视频信息失败: {e}")

# 格式化文件大小
def format_file_size(bytes_size):
    if bytes_size is None:
        return "未知"
    for unit in ['B', 'KB', 'MB', 'GB']:
        if bytes_size < 1024.0:
            return f"{bytes_size:.1f} {unit}"
        bytes_size /= 1024.0
    return f"{bytes_size:.1f} TB"

# 格式化时长
def format_duration(seconds):
    if seconds is None:
        return "未知"
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    seconds = seconds % 60
    if hours > 0:
        return f"{hours:02d}:{minutes:02d}:{seconds:02d}"
    else:
        return f"{minutes:02d}:{seconds:02d}"

# 异步下载视频
async def download_video(url: str, video_id: str):
    try:
        download_status[video_id] = {"status": "downloading", "progress": 0}
        
        # 配置yt-dlp选项
        ydl_opts = {
            'format': 'best[height<=720]',  # 下载最高720p质量
            'outtmpl': str(DOWNLOAD_DIR / '%(title)s.%(ext)s'),
            'restrictfilenames': True,
            'writeinfojson': False,
            'writesubtitles': False,
            'writeautomaticsub': False,
        }
        
        # 定义进度钩子
        def progress_hook(d):
            if d['status'] == 'downloading':
                if 'total_bytes' in d:
                    percent = (d['downloaded_bytes'] / d['total_bytes']) * 100
                    download_status[video_id]["progress"] = round(percent, 1)
                elif 'total_bytes_estimate' in d:
                    percent = (d['downloaded_bytes'] / d['total_bytes_estimate']) * 100
                    download_status[video_id]["progress"] = round(percent, 1)
            elif d['status'] == 'finished':
                download_status[video_id]["status"] = "processing"
                download_status[video_id]["progress"] = 100
        
        ydl_opts['progress_hooks'] = [progress_hook]
        
        # 使用yt-dlp下载视频
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            # 先获取视频信息
            info = ydl.extract_info(url, download=False)
            
            # 下载视频
            ydl.download([url])
            
            # 获取下载的文件路径
            filename = ydl.prepare_filename(info)
            file_path = Path(filename)
            
            # 如果文件不存在，尝试查找相似文件名
            if not file_path.exists():
                base_name = file_path.stem
                for file in DOWNLOAD_DIR.glob(f"{base_name}*"):
                    if file.is_file():
                        file_path = file
                        break
            
            # 获取文件大小
            file_size = file_path.stat().st_size if file_path.exists() else None
            
            # 创建视频信息对象
            video_info = VideoInfo(
                title=info.get('title', '未知标题'),
                duration=info.get('duration'),
                uploader=info.get('uploader', '未知作者'),
                description=info.get('description', '无描述')[:200] + '...' if info.get('description') and len(info.get('description', '')) > 200 else info.get('description', '无描述'),
                file_size=file_size,
                file_path=str(file_path.name),  # 只保存文件名
                downloaded_at=datetime.now().isoformat()
            )
            
            # 保存视频信息
            save_video_info(video_info)
            
            download_status[video_id] = {
                "status": "completed",
                "progress": 100,
                "video_info": video_info.dict()
            }
            
    except Exception as e:
        logger.error(f"下载失败: {e}")
        download_status[video_id] = {
            "status": "failed",
            "progress": 0,
            "error": str(e)
        }

# 路由
@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    load_downloaded_videos()
    
    # 为模板添加辅助函数
    def template_format_duration(seconds):
        return format_duration(seconds)
    
    def template_format_file_size(bytes_size):
        return format_file_size(bytes_size)
    
    return templates.TemplateResponse("index.html", {
        "request": request,
        "downloaded_videos": downloaded_videos,
        "format_duration": template_format_duration,
        "format_file_size": template_format_file_size
    })

@app.post("/download")
async def download_video_endpoint(video_url: VideoURL, background_tasks: BackgroundTasks):
    try:
        # 验证URL
        if not video_url.url.strip():
            raise HTTPException(status_code=400, detail="URL不能为空")
        
        # 生成唯一的下载ID
        video_id = str(len(download_status) + 1)
        
        # 添加后台任务
        background_tasks.add_task(download_video, video_url.url, video_id)
        
        return {"video_id": video_id, "message": "开始下载视频"}
        
    except Exception as e:
        logger.error(f"下载请求失败: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/status/{video_id}")
async def get_download_status(video_id: str):
    if video_id not in download_status:
        raise HTTPException(status_code=404, detail="下载任务不存在")
    
    return download_status[video_id]

@app.get("/videos")
async def get_downloaded_videos():
    load_downloaded_videos()
    return downloaded_videos

@app.delete("/videos/{video_filename}")
async def delete_video(video_filename: str):
    try:
        # 删除视频文件
        file_path = DOWNLOAD_DIR / video_filename
        if file_path.exists():
            file_path.unlink()
        
        # 从记录中移除
        global downloaded_videos
        downloaded_videos = [v for v in downloaded_videos if v['file_path'] != video_filename]
        
        # 保存更新后的列表
        info_file = DOWNLOAD_DIR / "videos_info.json"
        with open(info_file, 'w', encoding='utf-8') as f:
            json.dump(downloaded_videos, f, ensure_ascii=False, indent=2)
        
        return {"message": "视频删除成功"}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"删除失败: {str(e)}")

if __name__ == "__main__":
    # 启动时加载已下载的视频
    load_downloaded_videos()
    
    # 运行应用
    uvicorn.run(app, host="0.0.0.0", port=8000) 