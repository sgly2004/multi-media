import os

def delete_restored_images():
    # 基础路径
    base_path = '../frontend/src/assets/mock_pic'
    
    # 要处理的朝代文件夹
    dynasties = ['song', 'yuan', 'ming', 'qing']
    
    # 记录删除的文件数量
    deleted_count = 0
    
    # 遍历每个朝代文件夹
    for dynasty in dynasties:
        dynasty_path = os.path.join(base_path, dynasty)
        
        # 检查文件夹是否存在
        if not os.path.exists(dynasty_path):
            print(f"文件夹不存在: {dynasty_path}")
            continue
            
        # 遍历文件夹中的所有文件
        for filename in os.listdir(dynasty_path):
            if filename.endswith('_restored.png'):
                file_path = os.path.join(dynasty_path, filename)
                try:
                    os.remove(file_path)
                    deleted_count += 1
                    print(f"已删除: {file_path}")
                except Exception as e:
                    print(f"删除失败 {file_path}: {str(e)}")
    
    print(f"\n总共删除了 {deleted_count} 个restored图片文件")

if __name__ == "__main__":
    delete_restored_images()
