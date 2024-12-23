<template>
  <div class="gallery-container">
    <div class="paintings-grid">
      <div v-if="paintings.length === 0" class="no-paintings">
        暂无相关画作
      </div>
      <div 
        v-for="painting in paintings" 
        :key="painting.id"
        class="painting-card"
        :class="{ 'premium': painting.isPremium }"
        @click="handlePaintingClick(painting)"
      >
        <div class="image-container">
          <img 
            :src="painting.imageUrl" 
            :alt="painting.title"
            @error="handleImageError"
          >
          <div v-if="painting.isPremium" class="premium-badge">精品</div>
        </div>
        <div class="painting-info">
          <h3>{{ painting.title }}</h3>
          <p class="artist">{{ painting.artist }}</p>
          <p class="dynasty">{{ painting.dynasty }}</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'ScrollGallery',
  props: {
    paintings: {
      type: Array,
      required: true,
      default: () => []
    }
  },
  methods: {
    handlePaintingClick(painting) {
      console.log('点击画作:', painting);
      this.$emit('paintingClick', painting);
    },
    handleImageError(e) {
      console.error('图片加载失败:', e.target.src);
      e.target.src = require('@/assets/mock_pic/default.png');
    }
  },
  watch: {
    paintings: {
      immediate: true,
      handler(newPaintings) {
        console.log('画作列表更新:', newPaintings);
        if (newPaintings.length === 0) {
          console.log('警告: 没有找到符合条件的画作');
        }
      }
    }
  }
}
</script>

<style scoped>
.gallery-container {
  width: 100%;
  margin-top: 2rem;
}

.paintings-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 30px;
  padding: 20px;
}

.painting-card {
  position: relative;
  border-radius: 12px;
  overflow: hidden;
  box-shadow: 0 4px 12px rgba(0,0,0,0.1);
  cursor: pointer;
  transition: all 0.3s ease;
  background: white;
  animation: fadeIn 0.5s ease-out forwards;
  opacity: 0;
}

.painting-card.premium {
  border: 2px solid #FFD700;
  box-shadow: 0 4px 15px rgba(255, 215, 0, 0.3);
}

.image-container {
  position: relative;
  width: 100%;
  height: 280px;
  overflow: hidden;
}

.painting-card img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform 0.3s ease;
}

.painting-card:hover img {
  transform: scale(1.05);
}

.painting-info {
  padding: 15px;
  background: rgba(255,255,255,0.95);
  border-top: 1px solid rgba(0,0,0,0.1);
}

.painting-info h3 {
  margin: 0 0 8px 0;
  font-size: 18px;
  color: #2c3e50;
  font-family: "KaiTi", serif;
}

.painting-info .artist {
  margin: 0 0 4px 0;
  color: #666;
  font-size: 14px;
}

.painting-info .dynasty {
  margin: 0;
  color: #888;
  font-size: 14px;
}

.premium-badge {
  position: absolute;
  top: 10px;
  right: 10px;
  background: linear-gradient(135deg, #FFD700, #FFA500);
  color: #000;
  padding: 5px 12px;
  border-radius: 4px;
  font-size: 14px;
  font-weight: bold;
  box-shadow: 0 2px 4px rgba(0,0,0,0.2);
}

@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.painting-card:nth-child(n) {
  animation-delay: calc(0.1s * var(--i, 0));
}

.no-paintings {
  grid-column: 1 / -1;
  text-align: center;
  padding: 40px;
  font-size: 18px;
  color: #666;
  font-family: "KaiTi", serif;
}
</style> 