import requests
import base64

SUB_URL = "https://raw.githubusercontent.com/free18/v2ray/refs/heads/main/v.txt"

# 国家顺序
ORDER = [
    ("FR", ["france", "🇫🇷", " fr "]),
    ("US", ["united", "usa", "us", "🇺🇸"]),
    ("JP", ["japan", "jp", "🇯🇵"]),
    ("FI", ["finland", "fi", "🇫🇮"]),
    ("NL", ["netherlands", "nl", "🇳🇱"]),
]

print("Downloading subscription...")
resp = requests.get(SUB_URL, timeout=20)
b64_data = resp.text.strip()

print("Decoding...")
decoded = base64.b64decode(b64_data + "==").decode("utf-8", errors="ignore")
lines = [l.strip() for l in decoded.split("\n") if l.strip()]

valid = [
    l for l in lines
    if l.startswith(("vmess://", "vless://", "trojan://", "ss://"))
]

def match(line, keywords):
    remark = ""
    if "#" in line:
        remark = line.split("#")[-1].lower()
    return any(k in remark for k in keywords)

result = []
added = set()

for _, keywords in ORDER:
    for line in valid:
        if line in added:
            continue
        if match(line, keywords):
            result.append(line)
            added.add(line)

print(f"Filtered nodes: {len(result)}")

encoded = base64.b64encode("\n".join(result).encode()).decode()

with open("filtered.txt", "w", encoding="utf-8") as f:
    f.write(encoded)

print("Done.")
