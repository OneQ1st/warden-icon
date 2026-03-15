import json
import os

JSON_FILE = 'icons.json'

def safe_sync():
    if not os.path.exists(JSON_FILE):
        return
    
    with open(JSON_FILE, 'r', encoding='utf-8') as f:
        data = json.load(f)

    # 逻辑：只要文件夹不在了，就从列表里剔除该条目
    if isinstance(data, list):
        # 这里的 'name' 对应你 JSON 里的文件夹名字段
        new_data = [item for item in data if os.path.isdir(item.get('name', ''))]
        
        # 只有在数量变少时才重写文件
        if len(new_data) < len(data):
            with open(JSON_FILE, 'w', encoding='utf-8') as f:
                json.dump(new_data, f, indent=2, ensure_ascii=False)

if __name__ == "__main__":
    safe_sync()
