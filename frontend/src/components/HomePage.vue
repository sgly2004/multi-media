<template>
  <div class="home-container">
    <h1 class="main-title">数字画廊</h1>
    <div class="scroll-outer">
      <div class="scroll-container">
        <div class="scroll-content">
          <transition name="fade">
            <div v-if="!showGallery" class="timeline-section">
              <div class="timeline">
                <div class="timeline-line"></div>
                <div class="timeline-points">
                  <div
                    v-for="dynasty in dynasties"
                    :key="dynasty"
                    class="timeline-point"
                    :class="{ active: dynasty === currentDynasty }"
                    @click="handleDynastyChange(dynasty)"
                  >
                    <div class="point"></div>
                    <div class="dynasty-label">{{ dynasty }}</div>
                  </div>
                </div>
              </div>
              
              <TimelineCloud 
                :dynasty="currentDynasty"
                @wordClicked="handleWordClick"
                @dynastyChange="handleDynastyChange"
              />
            </div>
          </transition>
          <transition name="fade">
            <div v-if="showGallery" class="gallery-container">
              <div class="gallery-header">
                <h2>{{ selectedWord }}相关画作</h2>
                <button class="back-btn" @click="closeGallery">
                  返回词云
                </button>
              </div>
              <ScrollGallery 
                :paintings="filteredPaintings"
                @paintingClick="navigateToPainting"
              />
            </div>
          </transition>
        </div>
      </div>
    </div>
    
    <div class="create-button-container">
      <button class="create-btn" @click="goToCreate">
        自由创作
      </button>
    </div>
  </div>
</template>

<script>
import TimelineCloud from './TimelineCloud.vue'
import ScrollGallery from './ScrollGallery.vue'
import { mockDynasties } from '../mock_data/dynasties'
import { mockPaintings } from '../mock_data/paintings'

export default {
  name: 'HomePage',
  components: {
    TimelineCloud,
    ScrollGallery
  },
  data() {
    return {
      dynastyIndex: 0,
      showGallery: false,
      selectedWord: '',
      dynasties: mockDynasties,
      paintings: mockPaintings,
      defaultImage: new URL('../assets/mock_pic/default.png', import.meta.url).href
    }
  },
  computed: {
    currentDynasty() {
      console.log('Current dynasty:', this.dynasties[this.dynastyIndex])
      return this.dynasties[this.dynastyIndex]
    },
    filteredPaintings() {
      console.log('开始筛选画作:');
      console.log('- 当前朝代:', this.currentDynasty);
      console.log('- 选中的词:', this.selectedWord);
      
      // 首先按朝代筛选
      let filtered = this.paintings.filter(p => p.dynasty === this.currentDynasty);
      console.log(`- 当前朝代的画作数量: ${filtered.length}`);
      
      // 如果选择了关键词，进一步筛选
      if (this.selectedWord) {
        filtered = filtered.filter(p => {
          const hasTag = p.tags.includes(this.selectedWord);
          console.log(`- 画作 "${p.title}" ${hasTag ? '包含' : '不包含'}标签 "${this.selectedWord}"`);
          return hasTag;
        });
        console.log(`- 符合标签的画作数量: ${filtered.length}`);
      }
      
      // 处理图片路径
      filtered = filtered.map(painting => {
        const processedPainting = {
          ...painting,
          imageUrl: this.getImageUrl(painting)
        };
        console.log(`- 处理后的画作:`, processedPainting);
        return processedPainting;
      });
      
      return filtered;
    }
  },
  methods: {
    getImageUrl(painting) {
      try {
        // 添加朝代到拼音的映射
        const dynastyToPinyin = {
          '宋朝': 'song',
          '元朝': 'yuan',
          '明朝': 'ming',
          '清朝': 'qing'
        };

        console.log('处理画作:', {
          标题: painting.title,
          朝代: painting.dynasty,
          原始路径: painting.imageUrl
        });

        if (!painting.dynasty) {
          console.error('缺少朝代信息:', painting);
          return this.defaultImage;
        }

        const fileName = painting.imageUrl;
        const dynastyFolder = dynastyToPinyin[painting.dynasty];
        
        if (!dynastyFolder) {
          console.error('未找到对应的朝代文件夹:', painting.dynasty);
          return this.defaultImage;
        }
        
        const imageUrl = `/src/assets/mock_pic/${dynastyFolder}/${fileName}`;
        
        console.log('构建图片路径:', {
          文件名: fileName,
          朝代文件夹: dynastyFolder,
          完整路径: imageUrl
        });
        
        return imageUrl;
      } catch (err) {
        console.error('图片路径处理失败:', err);
        return this.defaultImage;
      }
    },
    prevDynasty() {
      console.log('Moving to previous dynasty')
      if (this.dynastyIndex > 0) {
        this.dynastyIndex--
        this.showGallery = false
      }
    },
    nextDynasty() {
      console.log('Moving to next dynasty')
      if (this.dynastyIndex < this.dynasties.length - 1) {
        this.dynastyIndex++
        this.showGallery = false
      }
    },
    handleWordClick(word) {
      console.log('词云点击:', word);
      this.selectedWord = word;
      this.showGallery = true;
      
      // 添加延时以确保数据更新后再检查结果
      this.$nextTick(() => {
        console.log('筛选后的画作数量:', this.filteredPaintings.length);
      });
    },
    navigateToPainting(painting) {
      console.log('Navigating to painting:', painting)
      this.$router.push({
        path: `/painting/${painting.id}`,
        query: { 
          imageUrl: `${painting.imageUrl}`
        }
      })
    },
    closeGallery() {
      this.showGallery = false;
      this.selectedWord = '';
    },
    goToCreate() {
      this.$router.push('/background-select')
    },
    handleDynastyChange(dynasty) {
      console.log('朝代切换:', dynasty);
      this.dynastyIndex = this.dynasties.indexOf(dynasty);
    }
  },
  mounted() {
    console.log('HomePage mounted')
    console.log('Initial dynasty:', this.currentDynasty)
    console.log('Available paintings:', this.paintings)
  }
}
</script>

<style scoped>
.home-container {
  min-height: 100vh;
  padding: 20px;
  background: #f9f4e6;
}

.scroll-outer {
  position: relative;
  margin: 40px auto;
  max-width: 1400px;
  width: 90vw;
}

.scroll-container {
  position: relative;
  background: linear-gradient(
    to right,
    rgba(244, 236, 218, 0.8),
    rgba(244, 236, 218, 0.95),
    rgba(244, 236, 218, 0.8)
  );
  border-radius: 12px;
  padding: 60px;
  box-shadow: 0 0 30px rgba(0, 0, 0, 0.15);
}

.scroll-container::before,
.scroll-container::after {
  content: '';
  position: absolute;
  top: 0;
  bottom: 0;
  width: 40px;
  background: #8b4513;
  opacity: 0.1;
}

.scroll-container::before {
  left: 0;
  border-radius: 8px 0 0 8px;
}

.scroll-container::after {
  right: 0;
  border-radius: 0 8px 8px 0;
}

.scroll-content {
  position: relative;
  z-index: 1;
}

.scroll-controls {
  display: flex;
  align-items: center;
  justify-content: center;
  margin-top: 30px;
  padding: 20px 0;
}

.scroll-btn {
  background: none;
  border: 2px solid #8b0000;
  color: #8b0000;
  padding: 10px 20px;
  margin: 0 20px;
  cursor: pointer;
  border-radius: 4px;
  font-size: 20px;
  transition: all 0.3s;
}

.scroll-btn:hover:not(:disabled) {
  background: #8b0000;
  color: #f9f4e6;
}

.scroll-btn:disabled {
  opacity: 0.3;
  cursor: not-allowed;
}

.dynasty-name {
  font-size: 28px;
  color: #2c3e50;
  font-family: "KaiTi", serif;
  min-width: 120px;
  text-align: center;
}

.gallery-container {
  margin-top: 40px;
  padding: 20px;
  background: rgba(255, 255, 255, 0.9);
  border-radius: 8px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
}

.fade-enter-active, .fade-leave-active {
  transition: opacity 0.5s ease;
}

.fade-enter-from, .fade-leave-to {
  opacity: 0;
}

.gallery-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
  padding: 0 20px;
}

.gallery-header h2 {
  font-family: "KaiTi", serif;
  color: #2c3e50;
  margin: 0;
}

.back-btn {
  background: none;
  border: 2px solid #8b0000;
  color: #8b0000;
  padding: 8px 16px;
  border-radius: 4px;
  cursor: pointer;
  font-family: "KaiTi", serif;
  transition: all 0.3s;
}

.back-btn:hover {
  background: #8b0000;
  color: #f9f4e6;
}

.main-title {
  text-align: center;
  color: #8b0000;
  font-family: "KaiTi", serif;
  font-size: 3rem;
  margin: 2rem 0;
  text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
}

.create-button-container {
  display: flex;
  justify-content: center;
  margin: 2rem 0;
}

.create-btn {
  background: #8b0000;
  color: white;
  border: none;
  padding: 1rem 4rem;
  font-size: 1.5rem;
  border-radius: 50px;
  cursor: pointer;
  font-family: "KaiTi", serif;
  transition: all 0.3s ease;
  box-shadow: 0 4px 12px rgba(139, 0, 0, 0.2);
}

.create-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 16px rgba(139, 0, 0, 0.3);
  background: #a00000;
}

.timeline-section {
  display: flex;
  flex-direction: column;
  gap: 0;
}

.timeline {
  position: relative;
  padding: 20px 0;
  margin: -20px 40px 0;
}

.timeline-line {
  position: absolute;
  top: 50%;
  left: 10%;
  right: 10%;
  height: 2px;
  background: #8b0000;
}

.timeline-points {
  position: relative;
  display: flex;
  justify-content: space-between;
  margin: 0 10%;
}

.timeline-point {
  position: relative;
  cursor: pointer;
  display: flex;
  flex-direction: column;
  align-items: center;
  z-index: 1;
}

.point {
  width: 16px;
  height: 16px;
  border-radius: 50%;
  background: #fff;
  border: 2px solid #8b0000;
  transition: all 0.3s ease;
}

.timeline-point.active .point {
  background: #8b0000;
  transform: scale(1.2);
}

.dynasty-label {
  margin-top: 8px;
  font-family: "KaiTi", serif;
  color: #2c3e50;
  transition: all 0.3s ease;
}

.timeline-point:hover .point {
  transform: scale(1.2);
}

.timeline-point.active .dynasty-label {
  color: #8b0000;
  font-weight: bold;
}
</style> 