import json
import os

# --- 配置项 ---
JSON_FILE = 'icons.json'  # 你的 JSON 文件名
ICON_DIR = 'icons'        # 图标存放的文件夹路径
KEY_NAME = 'name'         # JSON 中对应文件名的键名（根据实际情况修改）
# --------------

def sync_json():
    if not os.path.exists(JSON_FILE):
        print(f"错误: 找不到文件 {JSON_FILE}")
        return

    with open(JSON_FILE, 'r', encoding='utf-8') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            print("错误: JSON 格式非法")
            return

    # 过滤逻辑：只保留文件真实存在的条目
    # 假设 JSON 结构是列表 [{ "name": "icon1.png", ... }, ...]
    original_count = len(data)
    
    # 这里根据你的 JSON 结构调整判断逻辑
    new_data = [
        item for item in data 
        if os.path.exists(os.path.join(ICON_DIR, item[KEY_NAME]))
    ]

    # 写回文件
    with open(JSON_FILE, 'w', encoding='utf-8') as f:
        json.dump(new_data, f, indent=4, ensure_ascii=False)

    print(f"同步完成！")
    print(f"原索引条目: {original_count}")
    print(f"现索引条目: {len(new_data)}")
    print(f"已清理条目: {original_count - len(new_data)}")

if __name__ == "__main__":
    sync_json()
