import os, json

index_data = {}

# 1. 扫描当前所有的文件夹（自动跳过像 .git 这种隐藏文件夹）
folders = [f for f in os.listdir('.') if os.path.isdir(f) and not f.startswith('.')]

for folder in folders:
    icons = []
    # 2. 找出文件夹里所有的图标文件
    for file in os.listdir(folder):
        if file.endswith(('.png', '.svg')):
            icons.append({
                "name": file.replace('.png', '').replace('.svg', ''), # 去掉后缀名
                "path": f"{folder}/{file}"                             # 记录路径
            })
    
    # 3. 如果这个目录没被你删空，就把它加到新的记录里
    if icons:
        index_data[folder] = icons

# 4. 直接覆盖生成一份全新的 index.json
with open('index.json', 'w', encoding='utf-8') as f:
    json.dump(index_data, f, indent=2, ensure_ascii=False)

print("✅ 搞定！全新的 index.json 已经生成。")
