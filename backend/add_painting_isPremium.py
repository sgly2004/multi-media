import json
import os
import re

def update_is_premium():
    # 读取paintings.js文件
    with open('../frontend/src/mock_data/paintings.js', 'r', encoding='utf-8') as f:
        content = f.read()
        
        # 删除注释掉的内容
        content = re.sub(r'//.*?\n', '\n', content)  # 删除单行注释
        content = re.sub(r'/\*.*?\*/', '', content, flags=re.DOTALL)  # 删除多行注释
        
        # 提取JSON数组部分
        start = content.index('[')
        end = content.rindex(']') + 1
        paintings_json = content[start:end]
        paintings = json.loads(paintings_json)

    # 基础图片路径
    base_path = '../frontend/src/assets/mock_pic'

    # 遍历所有画作并更新isPremium
    for painting in paintings:
        dynasty_folder = painting['dynastyFolder']
        image_url = painting['imageUrl']
        
        # 构建restored图片路径
        image_name = os.path.splitext(image_url)[0]  # 移除.png扩展名
        restored_image = f"{image_name}_restored.png"
        full_path = os.path.join(base_path, dynasty_folder, restored_image)

        # 检查restored图片是否存在
        is_premium = os.path.exists(full_path)
        painting['isPremium'] = is_premium

    # 重新构建完整的js文件内容
    new_content = f"export const mockPaintings = {json.dumps(paintings, ensure_ascii=False, indent=2)}"

    # 写回文件
    with open('../frontend/src/mock_data/paintings.js', 'w', encoding='utf-8') as f:
        f.write(new_content)

if __name__ == "__main__":
    update_is_premium()
