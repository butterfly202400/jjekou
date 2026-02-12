import requests
import base64
import json

# —— 配置 —— #
SUB_URL = "https://raw.githubusercontent.com/free18/v2ray/refs/heads/main/v.txt"
ORDER = [
    ("FR", ["france", "🇫🇷", " fr"]),
    ("US", ["united", "usa", "us", "🇺🇸"]),
    ("JP", ["japan", "jp", "🇯🇵"]),
    ("FI", ["finland", "fi", "🇫🇮"]),
    ("NL", ["netherlands", "nl", "🇳🇱"]),
]

print("Downloading subscription...")
resp = requests.get(SUB_URL, timeout=20)
b64_data = resp.text.strip()

print("Decoding subscription...")
try:
    decoded = base64.b64decode(b64_data + "==").decode("utf-8", errors="ignore")
except Exception as e:
    print("❌ Base64 decode failed:", e)
    exit(1)

# —— 调试输出前500字符 —— #
print("Decoded subscription preview (first 500 chars):")
print(decoded[:500])
print("--------------------------------------------------")

lines = [l.strip() for l in decoded.split("\n") if l.strip()]

valid = []
for line in lines:
    if line.startswith("vmess://"):
        try:
            raw = line.replace("vmess://", "")
            config = json.loads(base64.b64decode(raw + "==").decode())
            remark = config.get("ps", "").lower()
            valid.append((line, remark))
        except Exception:
            continue
    elif line.startswith(("vless://", "trojan://", "ss://")):
        remark = ""
        if "#" in line:
            remark = line.split("#")[-1].lower()
        valid.append((line, remark))

print(f"Total valid nodes: {len(valid)}")

# —— 按国家筛选 + 去重 + 日志 —— #
result = []
added = set()

for country, keywords in ORDER:
    country_nodes = []
    for line, remark in valid:
        if line in added:
            continue
        if any(k in remark for k in keywords):
            result.append(line)
            added.add(line)
            country_nodes.append(remark)
    print(f"{country} nodes: {len(country_nodes)}")
    for r in country_nodes:
        print(f"  - {r}")

print(f"Total filtered nodes: {len(result)}")

# —— 重新编码输出 —— #
encoded = base64.b64encode("\n".join(result).encode()).decode()

with open("filtered.txt", "w", encoding="utf-8") as f:
    f.write(encoded)

print("Done. Filtered subscription saved to filtered.txt")
