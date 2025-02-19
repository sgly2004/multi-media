<template>
  <div class="detail-container">
    <div class="main-content">
      <div class="painting-section">
        <div class="painting-display">
          <div v-if="painting?.isPremium" class="mode-switch">
            <button @click="toggleMode">
              {{ isOriginal ? '修复模式' : '原画模式' }}
            </button>
          </div>
          <img 
            v-if="painting"
            :src="displayImage" 
            :alt="painting.title"
            :class="{'premium': painting.isPremium}"
            @mouseover="handleMouseOver"
            @mouseout="handleMouseOut"
          >
        </div>
      </div>
      
      <!-- <div class="chat-section">
        <ArtistChat 
          v-if="painting?.artistId"
          :artistId="painting.artistId"
        />
      </div> -->
    </div>
    
    <div class="info-section">
      <div v-if="painting" class="painting-info">
        <h2>{{ painting.title }}</h2>
        <p>作者：{{ painting.artist }}</p>
        <p>朝代：{{ painting.dynasty }}</p>
        <p>描述：{{ painting.description }}</p>
      </div>
      
      <!-- <div class="similar-paintings">
        <h3>相关作品</h3>
        <div class="similar-grid">
          <div 
            v-for="similar in similarPaintings" 
            :key="similar.id"
            class="similar-item"
            @click="loadPainting(similar.id)"
          >
            <img :src="similar.imageUrl" :alt="similar.title">
            <p>{{ similar.title }}</p>
          </div>
        </div>
      </div> -->
    </div>
  </div>
</template>

<script>
import ArtistChat from './ArtistChat.vue'
import { mockPaintings } from '../mock_data/paintings'

export default {
  name: 'PaintingDetail',
  components: {
    ArtistChat
  },
  data() {
    return {
      isOriginal: true,
      painting: null,
      similarPaintings: [],
      imageUrl: ''
    }
  },
  computed: {
    displayImage() {
      if (!this.painting?.isPremium) return this.imageUrl
      
      // 根据 isOriginal 状态决定显示原图还是修复图
      if (this.isOriginal) {
        return this.imageUrl
      } else {
        // 构建修复图片的完整路径
        return this.painting.restoredImage ? 
          `/src/assets/mock_pic/${this.painting.dynastyFolder}/${this.painting.restoredImage}` : 
          this.imageUrl
      }
    }
  },
  methods: {
    toggleMode() {
      this.isOriginal = !this.isOriginal
    },

    loadPainting(id) {
      console.log('Loading painting:', id)
      this.painting = mockPaintings.find(p => p.id === id)
      
      if (this.painting) {
        this.imageUrl = this.$route.query.imageUrl || 
          `/src/assets/mock_pic/${this.painting.dynastyFolder}/${this.painting.imageUrl}`
        
        this.similarPaintings = mockPaintings
          .filter(p => p.id !== id && p.tags.some(tag => this.painting.tags.includes(tag)))
          .slice(0, 4)
          .map(p => ({
            ...p,
            imageUrl: `/src/assets/mock_pic/${p.dynastyFolder}/${p.imageUrl}`
          }))
      }
    }
  },
  created() {
    const id = this.$route.params.id
    console.log('PaintingDetail created, id:', id)
    this.loadPainting(id)
  }
}
</script>

<style scoped>
.detail-container {
  padding: 40px;
  max-width: 1600px;
  margin: 0 auto;
  background: #f9f4e6;
}

.main-content {
  display: grid;
  grid-template-columns: 1fr;
  gap: 30px;
  margin-bottom: 40px;
  min-height: 600px;
}

.painting-section {
  position: relative;
  background: white;
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 4px 12px rgba(0,0,0,0.1);
  height: 100%;
  display: flex;
  flex-direction: column;
  align-items: center;
}

.painting-display {
  position: relative;
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
}

.painting-display img {
  width: 100%;
  height: auto;
  object-fit: contain;
  border-radius: 4px;
}

.painting-display img.premium {
  border: 2px solid #ffd700;
}

.mode-switch {
  position: absolute;
  top: 10px;
  right: 10px;
  z-index: 10;
}

.mode-switch button {
  background: rgba(139, 0, 0, 0.8);
  color: white;
  border: none;
  padding: 8px 16px;
  border-radius: 4px;
  cursor: pointer;
  transition: all 0.3s;
}

.mode-switch button:hover {
  background: rgba(139, 0, 0, 1);
}

.chat-section {
  height: 100%;
  display: flex;
  flex-direction: column;
}

.info-section {
  background: white;
  padding: 30px;
  border-radius: 8px;
  box-shadow: 0 4px 12px rgba(0,0,0,0.1);
}

.painting-info h2 {
  color: #2c3e50;
  margin-bottom: 20px;
  font-family: "KaiTi", serif;
}

.similar-paintings {
  margin-top: 30px;
}

.similar-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
  gap: 20px;
  margin-top: 20px;
}

.similar-item {
  cursor: pointer;
  transition: transform 0.3s;
}

.similar-item:hover {
  transform: translateY(-5px);
}

.similar-item img {
  width: 100%;
  height: 150px;
  object-fit: cover;
  border-radius: 4px;
}

.similar-item p {
  margin-top: 8px;
  text-align: center;
  font-family: "KaiTi", serif;
}
</style> 