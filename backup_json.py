import os
import shutil
from datetime import datetime, timedelta, timezone

# ===== 北京时间 (UTC+8) =====
beijing_tz = timezone(timedelta(hours=8))
now = datetime.now(beijing_tz)

timestamp = now.strftime("%Y-%m-%d_%H-%M-%S")

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
BACKUP_ROOT = os.path.join(ROOT_DIR, "backup")
BACKUP_DIR = os.path.join(BACKUP_ROOT, timestamp)
LOG_FILE = os.path.join(BACKUP_ROOT, "backup_log.txt")

# 创建目录
os.makedirs(BACKUP_DIR, exist_ok=True)

# ===== 备份 JSON 文件 =====
backup_count = 0

for filename in os.listdir(ROOT_DIR):
    filepath = os.path.join(ROOT_DIR, filename)

    if os.path.isfile(filepath) and filename.endswith(".json"):
        dest_path = os.path.join(BACKUP_DIR, filename)
        shutil.copy2(filepath, dest_path)
        backup_count += 1

# ===== 清理15天前备份 =====
deleted_count = 0
cutoff_time = now - timedelta(days=15)

if os.path.exists(BACKUP_ROOT):
    for folder in os.listdir(BACKUP_ROOT):
        folder_path = os.path.join(BACKUP_ROOT, folder)

        if os.path.isdir(folder_path):
            try:
                folder_time = datetime.strptime(folder, "%Y-%m-%d_%H-%M-%S")
                folder_time = folder_time.replace(tzinfo=beijing_tz)

                if folder_time < cutoff_time:
                    shutil.rmtree(folder_path)
                    deleted_count += 1
            except:
                pass

# ===== 写入日志 =====
log_entry = (
    f"时间: {now.strftime('%Y-%m-%d %H:%M:%S')} | "
    f"备份文件数: {backup_count} | "
    f"清理旧备份: {deleted_count}\n"
)

os.makedirs(BACKUP_ROOT, exist_ok=True)

with open(LOG_FILE, "a", encoding="utf-8") as f:
    f.write(log_entry)

print("备份完成")
print(log_entry)
