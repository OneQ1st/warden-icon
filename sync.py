import json
import os

# --- 配置 ---
JSON_FILE = 'icons.json'
# 这里的键名请根据你 json 里的实际情况修改（是 name 还是其他）
KEY_NAME = 'name' 

def do_sync():
    if not os.path.exists(JSON_FILE):
        print(f"❌ 找不到 {JSON_FILE}")
        return

    with open(JSON_FILE, 'r', encoding='utf-8') as f:
        try:
            data = json.load(f)
        except:
            print("❌ JSON 格式错误")
            return

    # 假设你的 icons.json 格式是： [{"name": "zhipianren.emby", ...}, ...]
    if isinstance(data, list):
        before_count = len(data)
        # 核心逻辑：检查同名的文件夹是否存在
        data = [item for item in data if os.path.isdir(item.get(KEY_NAME, ''))]
        after_count = len(data)
    else:
        print("⚠️ 警告：JSON 不是列表格式，请检查内容。")
        return

    # 原地覆盖，保留缩进
    with open(JSON_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    print(f"✅ 同步完成！清理了 {before_count - after_count} 条失效索引。")

if __name__ == "__main__":
    do_sync()
