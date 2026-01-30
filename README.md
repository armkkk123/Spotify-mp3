# 🎧 YouTube/Spotify Downloader PRO

โปรแกรมดาวน์โหลดเพลงและวิดีโอจาก YouTube และ Spotify ระดับ Production พร้อม Error Handling, Logging และ Retry Mechanism ที่สมบูรณ์

## ✨ Features

### Core Features
- ✅ ดาวน์โหลด MP3 (เสียงอย่างเดียว) หลายระดับคุณภาพ
- ✅ ดาวน์โหลด MP4 (วิดีโอ + เสียง) หลายความละเอียด
- ✅ รองรับการค้นหาด้วยชื่อเพลง
- ✅ รองรับลิงก์ YouTube โดยตรง
- ✅ รองรับลิงก์ Spotify (แปลงเป็น YouTube อัตโนมัติ)

### Advanced Features
- 🔄 **Auto Retry**: ลองใหม่อัตโนมัติเมื่อดาวน์โหลดไม่สำเร็จ (ตั้งค่าได้)
- 📝 **Comprehensive Logging**: บันทึก log ทั้งในไฟล์และ console พร้อมสี
- 🎯 **Structured Code**: เขียนด้วย OOP, Type Hints, และ Design Patterns
- ⚡ **Timeout Protection**: ป้องกันค้างเมื่อดาวน์โหลดนาน
- 📊 **Statistics**: แสดงสถิติการดาวน์โหลดเมื่อจบโปรแกรม
- 🎨 **Metadata Embedding**: ฝัง thumbnail และ metadata ลงไฟล์อัตโนมัติ
- 🛡️ **Error Handling**: จัดการ error ทุกจุดอย่างครอบคลุม

## 📋 Requirements

### Required Files
โปรแกรมต้องการไฟล์เหล่านี้ในโฟลเดอร์เดียวกัน:
- `yt-dlp.exe` - ดาวน์โหลดจาก [yt-dlp releases](https://github.com/yt-dlp/yt-dlp/releases)
- `ffmpeg.exe` - ดาวน์โหลดจาก [ffmpeg.org](https://ffmpeg.org/download.html)
- `ffprobe.exe` - มากับ ffmpeg

### Python Version
- Python 3.8 ขึ้นไป

### Python Packages
```bash
pip install -r requirements.txt
```

## 🚀 Installation

1. **โคลนหรือดาวน์โหลดโปรเจ็ค**
```bash
git clone <your-repo-url>
cd youtube-downloader-pro
```

2. **ติดตั้ง Dependencies**
```bash
pip install -r requirements.txt
```

3. **ดาวน์โหลด External Tools**
   - ดาวน์โหลด `yt-dlp.exe` และวางในโฟลเดอร์โปรเจ็ค
   - ดาวน์โหลด `ffmpeg.exe` และ `ffprobe.exe` และวางในโฟลเดอร์โปรเจ็ค

4. **รันโปรแกรม**
```bash
python youtube_downloader_pro.py
```

## 📖 Usage

### เมนูหลัก

#### 1. เลือกประเภทไฟล์
- **MP3** - ดาวน์โหลดเฉพาะเสียง
  - สูงสุด (320kbps)
  - กลาง (192kbps)
  - ประหยัด (128kbps)

- **MP4** - ดาวน์โหลดวิดีโอ + เสียง
  - สูงสุด (Best Available)
  - 1080p (Full HD)
  - 720p (HD)
  - 480p (SD)

#### 2. เลือกแหล่งที่มา
- **ค้นหาด้วยชื่อ** - ใส่ชื่อเพลง/วิดีโอ โปรแกรมจะค้นหาให้อัตโนมัติ
- **YouTube URL** - วางลิงก์ YouTube โดยตรง
- **Spotify URL** - วางลิงก์เพลง Spotify (จะแปลงเป็น YouTube)

### ตัวอย่างการใช้งาน

```
🎧 YouTube/Spotify Downloader PRO v2.0
==================================================

📌 เลือกประเภทไฟล์
1) MP3 (เสียงอย่างเดียว)
2) MP4 (วิดีโอ + เสียง)
3) ออกจากโปรแกรม
เลือก (1-3): 1

📌 เลือกแหล่งที่มา
1) 🔍 ค้นหาด้วยชื่อเพลง/วิดีโอ
2) 🔗 วางลิงก์ YouTube
3) 🎵 วางลิงก์ Spotify (เพลงเดียว)
เลือก (1-3): 1

🎵 ใส่ชื่อหรือ URL: ลูกทุ่งเพลิน

📌 เลือกคุณภาพเสียง
1) สูงสุด (320kbps)
2) กลาง (192kbps)
3) ประหยัด (128kbps)
เลือก (1-3): 1

INFO: 🚀 เริ่มดาวน์โหลด MP3 (ครั้งที่ 1/3)
INFO: ✅ ดาวน์โหลด MP3 สำเร็จ

📁 ไฟล์บันทึกที่: C:\path\to\downloads

🔁 ดาวน์โหลดต่อไหม? (y/n) [y]:
```

## 🏗️ Project Structure

```
youtube-downloader-pro/
├── youtube_downloader_pro.py   # Main application
├── requirements.txt            # Python dependencies
├── README.md                   # Documentation
├── config.json                 # User configuration (auto-generated)
├── download.log                # Download logs
├── downloads/                  # Downloaded files
├── yt-dlp.exe                  # yt-dlp binary
├── ffmpeg.exe                  # FFmpeg binary
└── ffprobe.exe                 # FFprobe binary
```

## 🎯 Code Architecture

### Design Patterns Used
- **Singleton Pattern**: Configuration management
- **Strategy Pattern**: Quality selection
- **Factory Pattern**: Command building
- **Template Method**: Download workflow

### Class Structure
```
DownloaderApp (Main Controller)
├── Config (Configuration)
├── Logger (Logging System)
├── DependencyChecker (Validation)
├── Downloader (Core Logic)
│   ├── download_audio()
│   ├── download_video()
│   └── _execute_download()
├── QualitySettings (Presets)
└── UI (User Interface)
```

## 🔧 Configuration

### Default Settings
```python
MAX_RETRIES = 3          # จำนวนครั้งที่ลองใหม่
TIMEOUT = 300            # Timeout (วินาที)
```

### Custom Configuration
สร้างไฟล์ `config.json`:
```json
{
  "max_retries": 5,
  "timeout": 600,
  "default_audio_quality": "1",
  "default_video_quality": "2"
}
```

## 📊 Logging

### Log Levels
- **DEBUG**: รายละเอียดทั้งหมด
- **INFO**: ข้อมูลทั่วไป
- **WARNING**: คำเตือน
- **ERROR**: ข้อผิดพลาด
- **CRITICAL**: ข้อผิดพลาดร้ายแรง

### Log Files
- **Console**: แสดงผลแบบมีสี (INFO ขึ้นไป)
- **File** (`download.log`): บันทึกทุก level พร้อม timestamp

## 🛠️ Advanced Usage

### Custom Output Template
แก้ไขใน code:
```python
# Audio
output_template = "%(artist)s - %(title)s.%(ext)s"

# Video
output_template = "%(title)s - %(upload_date)s.%(ext)s"
```

### Download Playlist
ปิด `--no-playlist` ใน `_build_base_command()`:
```python
def _build_base_command(self) -> list:
    return [
        str(self.config.YTDLP),
        # "--no-playlist",  # Comment this line
        ...
    ]
```

## 🐛 Troubleshooting

### ปัญหาที่พบบ่อย

**1. ไม่พบ yt-dlp.exe**
- ตรวจสอบว่าดาวน์โหลดและวางไฟล์ในโฟลเดอร์เดียวกับ script

**2. ดาวน์โหลดล้มเหลวทุกครั้ง**
- ตรวจสอบ Internet connection
- อัพเดท yt-dlp เป็นเวอร์ชั่นล่าสุด
- ตรวจสอบ log file สำหรับรายละเอียด error

**3. Timeout**
- เพิ่มค่า `TIMEOUT` ใน Config
- ตรวจสอบความเร็ว Internet

**4. ไม่มี Thumbnail/Metadata**
- ตรวจสอบว่ามี ffmpeg.exe และ ffprobe.exe

## 📝 TODO / Future Improvements

- [ ] Playlist support
- [ ] GUI version (Tkinter/PyQt)
- [ ] Parallel downloads
- [ ] Download queue
- [ ] Resume incomplete downloads
- [ ] Custom naming templates via UI
- [ ] Download history database
- [ ] Progress bar visualization
- [ ] Audio normalization option
- [ ] Subtitle download support

## 🤝 Contributing

Pull requests are welcome! For major changes, please open an issue first.

## 📄 License

MIT License - feel free to use this project for personal or commercial purposes.

## 🙏 Acknowledgments

- [yt-dlp](https://github.com/yt-dlp/yt-dlp) - The amazing YouTube downloader
- [FFmpeg](https://ffmpeg.org/) - Multimedia framework
- All contributors and users

## 📞 Support

หากพบปัญหาหรือมีคำถาม:
1. ตรวจสอบ [Troubleshooting](#-troubleshooting)
2. อ่าน log file (`download.log`)
3. เปิด issue บน GitHub

---

Made with ❤️ for music and video lovers
