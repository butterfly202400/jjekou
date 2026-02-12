import requests
import base64
import re
import time
import sys
import os

# 订阅 URL
URL = "https://raw.githubusercontent.com/free18/v2ray/refs/heads/main/v.txt"

# 想要提取的国家顺序
COUNTRIES = ["法国", "美国", "日本", "芬兰", "荷兰"]

# 保存文件
OUTPUT_FILE = "vmess_links.txt"
LOG_FILE = "fetch_log.txt"

# 最大重试次数
MAX_RETRIES = 3
RETRY_DELAY = 5  # 秒

def log(message):
    """打印并写入日志"""
    print(message)
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(message + "\n")

def fetch_subscription(url):
    """获取订阅内容，失败重试"""
    for attempt in range(1, MAX_RETRIES + 1):
        try:
            response = requests.get(url, timeout=15)
            response.raise_for_status()
            log(f"订阅获取成功 (尝试 {attempt})")
            return response.text
        except Exception as e:
            log(f"获取失败 (尝试 {attempt}): {e}")
            if attempt < MAX_RETRIES:
                log(f"{RETRY_DELAY} 秒后重试...")
                time.sleep(RETRY_DELAY)
            else:
                log("超过最大重试次数，退出程序。")
                sys.exit(1)

def decode_base64(content):
    """解码 Base64"""
    try:
        decoded_bytes = base64.b64decode(content)
        return decoded_bytes.decode('utf-8', errors='ignore')
    except Exception as e:
        log("Base64 解码失败: " + str(e))
        return ""

def extract_vmess_nodes(decoded_text, countries):
    """提取指定国家的 vmess 节点"""
    nodes = []
    for country in countries:
        pattern = rf"vmess://[^\s]*{country}[^\s]*"
        found = re.findall(pattern, decoded_text)
        nodes.extend(found)
    return nodes

def main():
    log("===== 开始执行脚本 =====")
    content = fetch_subscription(URL)
    decoded = decode_base64(content)
    
    log("前500字符调试:\n" + decoded[:500])
    
    nodes = extract_vmess_nodes(decoded, COUNTRIES)
    
    if not nodes:
        log("未提取到任何节点，终止提交。")
        sys.exit(0)
    
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        for node in nodes:
            f.write(node + "\n")
    
    log(f"共提取 {len(nodes)} 个节点，已保存到 {OUTPUT_FILE}")
    log("===== 脚本执行完成 =====\n")

if __name__ == "__main__":
    main()
