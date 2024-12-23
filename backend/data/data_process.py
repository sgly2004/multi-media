import pandas as pd
from collections import Counter
import json
from pathlib import Path

def process_cloud_words(df):
    # 按朝代分组统计标签
    dynasty_tags = {}
    dynasties = {
        '宋代': 'song',
        '元代': 'yuan',
        '明代': 'ming',
        '清代': 'qing'
    }
    
    for dynasty in dynasties.keys():
        # 获取该朝代的所有标签
        dynasty_df = df[df['朝代'] == dynasty]
        all_tags = []
        for tags in dynasty_df['标签'].dropna():
            if isinstance(tags, str):
                all_tags.extend(tags.split('、'))
        
        # 统计标签频率
        tag_counts = Counter(all_tags)
        
        # 转换为所需格式
        max_size = 5  # 最大字体大小
        total = max(tag_counts.values()) if tag_counts else 1
        
        cloud_words = [
            {
                'text': tag,
                'size': max(2, int((count / total) * max_size))
            }
            for tag, count in tag_counts.most_common(10)  # 取前10个标签
        ]
        
        dynasty_tags[dynasty] = cloud_words
    
    return dynasty_tags

def process_paintings(df):
    paintings = []
    dynasties = {
        '宋代': 'song',
        '元代': 'yuan',
        '明代': 'ming',
        '清代': 'qing'
    }
    
    for _, row in df.iterrows():
        dynasty_folder = dynasties.get(row['朝代'], '')
        if not dynasty_folder:
            continue
            
        image_name = f"{row['题目']}.png" if pd.notna(row['题目']) else ""
        image_path = f"@/assets/mock_pic/{dynasty_folder}/{image_name}"
        
        painting = {
            'id': str(row.name + 1),  # 使用索引+1作为ID
            'title': row['题目'] if pd.notna(row['题目']) else '',
            'artist': row['作者'] if pd.notna(row['作者']) else '佚名',
            'artistId': f"artist_{row.name}",  # 生成艺术家ID
            'dynasty': row['朝代'] if pd.notna(row['朝代']) else '',
            'imageUrl': image_path,
            'tags': row['标签'].split('、') if pd.notna(row['标签']) else [],
            'isPremium': bool(row.name % 2),  # 随机设置premium属性
            'description': f"这是一幅{row['朝代']}的{row['题目']}...",
        }
        
        # 为部分作品添加修复图和动画
        if row.name % 3 == 0:  # 每三个作品添加一次
            painting['restoredImage'] = f"{image_path.replace('.png', '_restored.png')}"
            painting['animation'] = f"{image_path.replace('.png', '_animation.mp4')}"
            
        paintings.append(painting)
    
    return paintings

def generate_js_files():
    # 读取Excel文件
    df = pd.read_excel('backend/data/merged_output.xlsx')
    
    # 处理词云数据
    cloud_words = process_cloud_words(df)
    cloud_words_js = f"export const mockCloudWords = {json.dumps(cloud_words, ensure_ascii=False, indent=2)}"
    
    # 处理画作数据
    paintings = process_paintings(df)
    paintings_js = f"""import painting1 from '@/assets/mock_pic/song/painting1.png'
import painting1Restored from '@/assets/mock_pic/song/painting1_restored.png'
import painting1Animation from '@/assets/mock_pic/song/painting1_animation.mp4'

export const mockPaintings = {json.dumps(paintings, ensure_ascii=False, indent=2)}"""
    
    # 写入JS文件
    with open('frontend/src/mock_data/cloudWords.js', 'w', encoding='utf-8') as f:
        f.write(cloud_words_js)
        
    with open('frontend/src/mock_data/paintings.js', 'w', encoding='utf-8') as f:
        f.write(paintings_js)

if __name__ == '__main__':
    generate_js_files()