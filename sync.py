import json
import os

# 锁定文件名
TARGET = 'icons.json'

def sync():
    if not os.path.exists(TARGET):
        print(f"找不到 {TARGET}")
        return
    
    with open(TARGET, 'r', encoding='utf-8') as f:
        try:
            data = json.load(f)
        except:
            print("JSON 解析失败")
            return

    # 逻辑：只保留那些文件夹还存在的名字
    if isinstance(data, list):
        # 只要这个名字对应的文件夹还在，就留着
        new_data = [name for name in data if os.path.isdir(str(name))]
        
        # 只有在真的有变化时才写入
        if len(new_data) < len(data):
            with open(TARGET, 'w', encoding='utf-8') as f:
                json.dump(new_data, f, indent=2, ensure_ascii=False)
                f.write('\n') # 规范换行
            print(f"清理成功：从 {len(data)} 减少到 {len(new_data)}")
        else:
            print("索引已经是干净的，无需操作")

if __name__ == "__main__":
    sync()
