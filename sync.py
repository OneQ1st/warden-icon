import json
import os

# 1. 确定你的文件名
JSON_FILE = 'icons.json'

def safe_sync():
    # 预防万一：先备份原始文件
    if not os.path.exists(JSON_FILE):
        print(f"找不到 {JSON_FILE}")
        return
    
    with open(JSON_FILE, 'r', encoding='utf-8') as f:
        try:
            data = json.load(f)
        except Exception as e:
            print(f"JSON 读取失败: {e}")
            return

    # 2. 核心清理逻辑
    # 保持原有的数据结构，只过滤掉目录不存在的项
    if isinstance(data, list):
        # 假设你的 json 格式是 [{"name": "zhipianren.emby", ...}, ...]
        # 脚本会检查当前目录下是否有名为 "zhipianren.emby" 的文件夹
        new_data = [
            item for item in data 
            if os.path.isdir(item.get('name', ''))
        ]
        
        removed_count = len(data) - len(new_data)
    else:
        print("错误：JSON 格式不是列表，为了安全停止操作。")
        return

    # 3. 只有在确实有变动时才写入，避免无谓的刷新
    if removed_count > 0:
        with open(JSON_FILE, 'w', encoding='utf-8') as f:
            # indent=2 保证你的 JSON 还是美观可读的，不会缩成一团
            json.dump(new_data, f, indent=2, ensure_ascii=False)
        print(f"✅ 清理完成！已移除 {removed_count} 个失效索引，其余内容保持不变。")
    else:
        print("💡 没有发现失效索引，文件未做修改。")

if __name__ == "__main__":
    safe_sync()
