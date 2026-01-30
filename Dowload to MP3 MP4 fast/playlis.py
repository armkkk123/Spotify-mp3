"""
YouTube/Spotify Downloader PRO
Production-grade media downloader with comprehensive error handling and logging
"""

import os
import sys
import subprocess
import json
import logging
from datetime import datetime
from pathlib import Path
from typing import Optional, Dict, Tuple
from dataclasses import dataclass
from enum import Enum


# ================= CONFIGURATION =================
@dataclass
class Config:
    """Application configuration"""
    BASE_DIR: Path = Path(__file__).parent.absolute()
    YTDLP: Path = BASE_DIR / "yt-dlp.exe"
    FFMPEG: Path = BASE_DIR / "ffmpeg.exe"
    FFPROBE: Path = BASE_DIR / "ffprobe.exe"
    DOWNLOAD_DIR: Path = BASE_DIR / "downloads"
    LOG_FILE: Path = BASE_DIR / "download.log"
    CONFIG_FILE: Path = BASE_DIR / "config.json"
    
    # Download settings
    MAX_RETRIES: int = 3
    TIMEOUT: int = 300  # seconds
    
    def __post_init__(self):
        """Create necessary directories"""
        self.DOWNLOAD_DIR.mkdir(exist_ok=True)


class FileType(Enum):
    """Download file types"""
    MP3 = "mp3"
    MP4 = "mp4"


class DownloadMode(Enum):
    """Download modes"""
    SEARCH = 1
    YOUTUBE_URL = 2
    SPOTIFY_URL = 3


# ================= LOGGING SETUP =================
class ColoredFormatter(logging.Formatter):
    """Custom formatter with colors for console output"""
    
    COLORS = {
        'DEBUG': '\033[36m',    # Cyan
        'INFO': '\033[32m',     # Green
        'WARNING': '\033[33m',  # Yellow
        'ERROR': '\033[31m',    # Red
        'CRITICAL': '\033[35m', # Magenta
    }
    RESET = '\033[0m'
    
    def format(self, record):
        if record.levelname in self.COLORS:
            record.levelname = f"{self.COLORS[record.levelname]}{record.levelname}{self.RESET}"
        return super().format(record)


def setup_logging(config: Config) -> logging.Logger:
    """Setup logging with file and console handlers"""
    logger = logging.getLogger('Downloader')
    logger.setLevel(logging.DEBUG)
    
    # File handler
    file_handler = logging.FileHandler(
        config.LOG_FILE, 
        encoding='utf-8'
    )
    file_handler.setLevel(logging.DEBUG)
    file_formatter = logging.Formatter(
        '%(asctime)s | %(levelname)-8s | %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    file_handler.setFormatter(file_formatter)
    
    # Console handler with colors
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_formatter = ColoredFormatter(
        '%(levelname)s: %(message)s'
    )
    console_handler.setFormatter(console_formatter)
    
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    
    return logger


# ================= DEPENDENCY CHECKER =================
class DependencyChecker:
    """Check and validate required dependencies"""
    
    def __init__(self, config: Config, logger: logging.Logger):
        self.config = config
        self.logger = logger
    
    def check_all(self) -> bool:
        """Check all required files"""
        missing = []
        
        for tool in [self.config.YTDLP, self.config.FFMPEG, self.config.FFPROBE]:
            if not tool.exists():
                missing.append(tool.name)
        
        if missing:
            self.logger.error("❌ ไม่พบไฟล์ที่จำเป็น:")
            for m in missing:
                self.logger.error(f"   - {m}")
            return False
        
        self.logger.info("✅ ตรวจสอบไฟล์ครบถ้วน")
        return True
    
    def check_ytdlp_version(self) -> Optional[str]:
        """Check yt-dlp version"""
        try:
            result = subprocess.run(
                [str(self.config.YTDLP), "--version"],
                capture_output=True,
                text=True,
                timeout=10
            )
            version = result.stdout.strip()
            self.logger.info(f"yt-dlp version: {version}")
            return version
        except Exception as e:
            self.logger.warning(f"ไม่สามารถตรวจสอบเวอร์ชั่น yt-dlp: {e}")
            return None


# ================= QUALITY SETTINGS =================
class QualitySettings:
    """Quality presets for downloads"""
    
    AUDIO_QUALITIES = {
        "1": {"bitrate": "0", "label": "สูงสุด (320kbps)"},
        "2": {"bitrate": "5", "label": "กลาง (192kbps)"},
        "3": {"bitrate": "9", "label": "ประหยัด (128kbps)"},
    }
    
    VIDEO_QUALITIES = {
        "1": {"format": "bv*+ba/b", "label": "สูงสุด (Best Available)"},
        "2": {"format": "bv*[height<=1080]+ba/b", "label": "1080p (Full HD)"},
        "3": {"format": "bv*[height<=720]+ba/b", "label": "720p (HD)"},
        "4": {"format": "bv*[height<=480]+ba/b", "label": "480p (SD)"},
    }
    
    @classmethod
    def get_audio_quality(cls, choice: str = "1") -> str:
        """Get audio quality bitrate"""
        return cls.AUDIO_QUALITIES.get(choice, cls.AUDIO_QUALITIES["1"])["bitrate"]
    
    @classmethod
    def get_video_format(cls, choice: str = "1") -> str:
        """Get video format string"""
        return cls.VIDEO_QUALITIES.get(choice, cls.VIDEO_QUALITIES["1"])["format"]


# ================= USER INTERFACE =================
class UI:
    """User interface helper"""
    
    @staticmethod
    def clear_screen():
        """Clear console screen"""
        os.system('cls' if os.name == 'nt' else 'clear')
    
    @staticmethod
    def print_header():
        """Print application header"""
        print("\n" + "="*50)
        print("🎧 YouTube/Spotify Downloader PRO v2.0")
        print("="*50 + "\n")
    
    @staticmethod
    def print_menu(title: str, options: Dict[str, str]) -> str:
        """Print menu and get user choice"""
        print(f"\n📌 {title}")
        for key, value in options.items():
            print(f"{key}) {value}")
        
        choice = input(f"เลือก (1-{len(options)}): ").strip()
        return choice
    
    @staticmethod
    def get_input(prompt: str, required: bool = True) -> Optional[str]:
        """Get user input with validation"""
        while True:
            value = input(f"\n{prompt}: ").strip()
            if value or not required:
                return value
            print("❌ กรุณาใส่ข้อมูล")
    
    @staticmethod
    def confirm(prompt: str, default: bool = True) -> bool:
        """Get yes/no confirmation"""
        choice = input(f"{prompt} (y/n) [{['n', 'y'][default]}]: ").lower().strip()
        if not choice:
            return default
        return choice == 'y'


# ================= DOWNLOADER =================
class Downloader:
    """Main downloader class"""
    
    def __init__(self, config: Config, logger: logging.Logger):
        self.config = config
        self.logger = logger
        self.stats = {
            "total": 0,
            "success": 0,
            "failed": 0
        }
    
    def _build_base_command(self) -> list:
        """Build base yt-dlp command"""
        return [
            str(self.config.YTDLP),
            "--no-playlist",
            "--progress",
            "--newline",
            "--ffmpeg-location", str(self.config.BASE_DIR),
            "--extractor-args", "youtube:player_client=android",
        ]
    
    def download_audio(
        self, 
        query: str, 
        quality: str,
        output_template: Optional[str] = None
    ) -> bool:
        """Download audio (MP3)"""
        
        if output_template is None:
            output_template = "%(artist)s - %(title)s.%(ext)s"
        
        cmd = self._build_base_command() + [
            "-x",
            "--audio-format", "mp3",
            "--audio-quality", quality,
            "--embed-thumbnail",
            "--add-metadata",
            "-o", str(self.config.DOWNLOAD_DIR / output_template),
            query
        ]
        
        return self._execute_download(cmd, "MP3")
    
    def download_video(
        self,
        query: str,
        format_spec: str,
        output_template: Optional[str] = None
    ) -> bool:
        """Download video (MP4)"""
        
        if output_template is None:
            output_template = "%(title)s.%(ext)s"
        
        cmd = self._build_base_command() + [
            "-f", format_spec,
            "--merge-output-format", "mp4",
            "--embed-thumbnail",
            "--add-metadata",
            "-o", str(self.config.DOWNLOAD_DIR / output_template),
            query
        ]
        
        return self._execute_download(cmd, "MP4")
    
    def _execute_download(self, cmd: list, file_type: str) -> bool:
        """Execute download command with retry logic"""
        
        for attempt in range(1, self.config.MAX_RETRIES + 1):
            try:
                self.logger.info(f"🚀 เริ่มดาวน์โหลด {file_type} (ครั้งที่ {attempt}/{self.config.MAX_RETRIES})")
                
                process = subprocess.run(
                    cmd,
                    cwd=self.config.BASE_DIR,
                    timeout=self.config.TIMEOUT,
                    capture_output=True,
                    text=True
                )
                
                if process.returncode == 0:
                    self.logger.info(f"✅ ดาวน์โหลด {file_type} สำเร็จ")
                    self.stats["success"] += 1
                    return True
                else:
                    error_msg = process.stderr or "Unknown error"
                    self.logger.warning(f"⚠️ ดาวน์โหลดไม่สำเร็จ: {error_msg}")
                    
            except subprocess.TimeoutExpired:
                self.logger.error(f"⏱️ Timeout (เกิน {self.config.TIMEOUT} วินาที)")
            except Exception as e:
                self.logger.error(f"❌ Error: {str(e)}")
            
            if attempt < self.config.MAX_RETRIES:
                self.logger.info(f"🔄 ลองใหม่...")
        
        self.stats["failed"] += 1
        return False
    
    def get_stats(self) -> Dict[str, int]:
        """Get download statistics"""
        return self.stats.copy()


# ================= MAIN APPLICATION =================
class DownloaderApp:
    """Main application class"""
    
    def __init__(self):
        self.config = Config()
        self.logger = setup_logging(self.config)
        self.downloader = Downloader(self.config, self.logger)
        self.ui = UI()
    
    def run(self):
        """Run the application"""
        
        # Check dependencies
        checker = DependencyChecker(self.config, self.logger)
        if not checker.check_all():
            input("\nกด Enter เพื่อออก...")
            sys.exit(1)
        
        checker.check_ytdlp_version()
        
        # Main loop
        self.ui.print_header()
        
        while True:
            try:
                if not self._main_menu():
                    break
            except KeyboardInterrupt:
                self.logger.info("\n⚠️ ยกเลิกโดยผู้ใช้")
                break
            except Exception as e:
                self.logger.error(f"❌ เกิดข้อผิดพลาด: {e}")
        
        self._show_stats()
        input("\nกด Enter เพื่อปิดโปรแกรม...")
    
    def _main_menu(self) -> bool:
        """Main menu logic"""
        
        # File type selection
        file_type_choice = self.ui.print_menu(
            "เลือกประเภทไฟล์",
            {
                "1": "MP3 (เสียงอย่างเดียว)",
                "2": "MP4 (วิดีโอ + เสียง)",
                "3": "ออกจากโปรแกรม"
            }
        )
        
        if file_type_choice == "3":
            return False
        
        if file_type_choice not in ("1", "2"):
            self.logger.warning("❌ เลือกไม่ถูกต้อง")
            return True
        
        # Source selection
        mode_choice = self.ui.print_menu(
            "เลือกแหล่งที่มา",
            {
                "1": "🔍 ค้นหาด้วยชื่อเพลง/วิดีโอ",
                "2": "🔗 วางลิงก์ YouTube",
                "3": "🎵 วางลิงก์ Spotify (เพลงเดียว)"
            }
        )
        
        if mode_choice not in ("1", "2", "3"):
            self.logger.warning("❌ เลือกไม่ถูกต้อง")
            return True
        
        # Get query
        query = self.ui.get_input("🎵 ใส่ชื่อหรือ URL")
        if not query:
            return True
        
        # Prepare search query
        if mode_choice == "1":
            search_query = f"ytsearch1:{query}"
        else:
            search_query = query
        
        # Download
        success = False
        self.downloader.stats["total"] += 1
        
        if file_type_choice == "1":
            # Audio download
            quality_choice = self.ui.print_menu(
                "เลือกคุณภาพเสียง",
                {k: v["label"] for k, v in QualitySettings.AUDIO_QUALITIES.items()}
            )
            quality = QualitySettings.get_audio_quality(quality_choice)
            success = self.downloader.download_audio(search_query, quality)
        else:
            # Video download
            format_choice = self.ui.print_menu(
                "เลือกคุณภาพวิดีโอ",
                {k: v["label"] for k, v in QualitySettings.VIDEO_QUALITIES.items()}
            )
            format_spec = QualitySettings.get_video_format(format_choice)
            success = self.downloader.download_video(search_query, format_spec)
        
        if success:
            print(f"\n📁 ไฟล์บันทึกที่: {self.config.DOWNLOAD_DIR}")
        
        # Continue?
        return self.ui.confirm("\n🔁 ดาวน์โหลดต่อไหม?", default=True)
    
    def _show_stats(self):
        """Show download statistics"""
        stats = self.downloader.get_stats()
        
        if stats["total"] > 0:
            print("\n" + "="*50)
            print("📊 สถิติการดาวน์โหลด")
            print("="*50)
            print(f"ทั้งหมด:   {stats['total']}")
            print(f"สำเร็จ:    {stats['success']} ✅")
            print(f"ล้มเหลว:  {stats['failed']} ❌")
            success_rate = (stats['success'] / stats['total']) * 100
            print(f"อัตราสำเร็จ: {success_rate:.1f}%")
            print("="*50)


# ================= ENTRY POINT =================
def main():
    """Application entry point"""
    app = DownloaderApp()
    app.run()


if __name__ == "__main__":
    main()