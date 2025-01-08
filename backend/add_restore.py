import os
import shutil

def add_restore_suffix():
    # 源文件夹基础路径
    source_base = '../frontend/src/assets/restored'
    # 目标文件夹基础路径
    target_base = '../frontend/src/assets/mock_pic'
    
    # 要处理的朝代文件夹
    dynasties = ['song', 'yuan', 'ming', 'qing']
    
    # 记录处理的文件数量
    processed_count = 0
    
    # 遍历每个朝代文件夹
    for dynasty in dynasties:
        # 构建源路径（包含upscayl文件夹）
        source_path = os.path.join(source_base, dynasty, 'upscayl_png_realesrgan-x4plus_4x')
        # 构建目标路径
        target_path = os.path.join(target_base, dynasty)
        
        # 检查源文件夹是否存在
        if not os.path.exists(source_path):
            print(f"源文件夹不存在: {source_path}")
            continue
            
        # 确保目标文件夹存在
        os.makedirs(target_path, exist_ok=True)
        
        # 遍历源文件夹中的所有文件
        for filename in os.listdir(source_path):
            if filename.endswith('.png'):
                # 构建新文件名（添加_restored后缀）
                name_without_ext = os.path.splitext(filename)[0]
                new_filename = f"{name_without_ext}_restored.png"
                
                # 构建完整的源文件和目标文件路径
                source_file = os.path.join(source_path, filename)
                target_file = os.path.join(target_path, new_filename)
                
                try:
                    # 复制文件
                    shutil.copy2(source_file, target_file)
                    processed_count += 1
                    print(f"已处理: {filename} -> {new_filename}")
                except Exception as e:
                    print(f"处理失败 {filename}: {str(e)}")
    
    print(f"\n总共处理了 {processed_count} 个文件")

if __name__ == "__main__":
    add_restore_suffix()
