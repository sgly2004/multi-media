import os
import json

def clean_unused_images():
    # 读取paintings.js文件获取所有有效的图片名
    with open('../frontend/src/mock_data/paintings.js', 'r', encoding='utf-8') as f:
        content = f.read()
        start = content.index('[')
        end = content.rindex(']') + 1
        paintings_json = content[start:end]
        paintings = json.loads(paintings_json)

    # 获取所有有效的图片名列表
    valid_images = set()
    for painting in paintings:
        # 添加原始图片
        valid_images.add(painting['imageUrl'])
        # 添加restored版本
        image_name = os.path.splitext(painting['imageUrl'])[0]
        valid_images.add(f"{image_name}_restored.png")
        # 添加animation版本
        valid_images.add(f"{image_name}_animation.mp4")

    # 基础路径
    base_path = '../frontend/src/assets/mock_pic'
    
    # 要处理的朝代文件夹
    dynasties = ['song', 'yuan', 'ming', 'qing']
    
    # 记录删除的文件数量
    deleted_count = 0
    exist_count = 0
    
    # 遍历每个朝代文件夹
    for dynasty in dynasties:
        dynasty_path = os.path.join(base_path, dynasty)
        
        # 检查文件夹是否存在
        if not os.path.exists(dynasty_path):
            print(f"文件夹不存在: {dynasty_path}")
            continue
            
        # 遍历文件夹中的所有文件
        for filename in os.listdir(dynasty_path):
            # 如果文件名不在有效列表中
            if filename not in valid_images:
                file_path = os.path.join(dynasty_path, filename)
                try:
                    os.remove(file_path)
                    deleted_count += 1
                    print(f"已删除冗余文件: {file_path}")
                except Exception as e:
                    print(f"删除失败 {file_path}: {str(e)}")
            else:
                exist_count += 1
    
    print(f"\n总共删除了 {deleted_count} 个冗余文件")
    print(f"总共存在 {exist_count} 个有效文件")

if __name__ == "__main__":
    clean_unused_images()
