import json

# ====================================================
# 1. 维护区域：以后你只需修改这里的 线路名 和 原始链接
# ====================================================
sub_configs = {
    "fty.json": {"name": "03_饭太硬", "url": "http://www.饭太硬.com/tv"},
    "wex.json": {"name": "04_王二小", "url": "https://9280.kstore.vip/newwex.json"},
    "ok01.json": {"name": "05_OK线路", "url": "https://10352.kstore.vip/tv"},
    "ok02.json": {"name": "06_OK备用", "url": "http://ok521.top/tv"},
    "ok03.json": {"name": "07_OK备用2", "url": "http://ok213.top/ok"},
    "cns.json": {"name": "08_菜妮丝", "url": "https://tv.xn--yhqu5zs87a.top"}
}

def generate_all():
    # --- 第一步：生成 03-08 的独立子 JSON 文件 ---
    for filename, content in sub_configs.items():
        data = {
            "urls": [
                {
                    "name": content["name"],
                    "url": content["url"]
                }
            ]
        }
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print(f"✅ 子接口已更新: {filename}")

    # --- 第二步：构建完整的主接口 out.json 内容 ---
    # 固定的 01-02 线路
    main_data = {
        "urls": [
            {
                "name": "01_特制净化",
                "url": "https://ghfast.top/https://raw.githubusercontent.com/butterfly202400/jiekou/main/tzjh.json"
            },
            {
                "name": "02_王二小净化",
                "url": "https://ghfast.top/https://raw.githubusercontent.com/butterfly202400/jiekou/main/wexjh.json"
            }
        ]
    }

    # 自动将 sub_configs 里的 03-08 线路追加到 out.json 中
    for filename, content in sub_configs.items():
        main_data["urls"].append({
            "name": content["name"],
            "url": f"https://ghfast.top/https://raw.githubusercontent.com/butterfly202400/jiekou/main/{filename}"
        })

    # --- 第三步：写入并覆盖 out.json ---
    with open('out.json', 'w', encoding='utf-8') as f:
        json.dump(main_data, f, ensure_ascii=False, indent=2)
    
    print("🚀 恭喜！主接口 out.json 已同步生成并排序完成。")

if __name__ == "__main__":
    generate_all()
