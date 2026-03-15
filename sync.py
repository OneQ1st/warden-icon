import json
import os

# --- 配置 ---
JSON_FILE = 'icons.json'
# 扫描当前目录下所有的子文件夹（排除隐藏文件夹）
SEARCH_DIRS = [d for d in os.listdir('.') if os.path.isdir(d) and not d.startswith('.')]

def sync():
    new_data = {}

    for folder in SEARCH_DIRS:
        icons = []
        # 检查目录下是否存在图片
        if not os.path.exists(folder):
            continue
            
        files = sorted(os.listdir(folder))
        for f in files:
            if f.lower().endswith(('.png', '.svg', '.jpg')):
                # 构造索引条目
                icons.append({
                    "name": os.path.splitext(f)[0],
                    "path": f"{folder}/{f}"
                })
        
        # 只有文件夹里有图标，才写入索引
        if icons:
            new_data[folder] = icons

    with open(JSON_FILE, 'w', encoding='utf-8') as f:
        json.dump(new_data, f, indent=2, ensure_ascii=False)
    
    print(f"✅ 同步成功，当前索引包含 {len(new_data)} 个分类")

if __name__ == "__main__":
    sync()
