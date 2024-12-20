<template>
  <div class="related-paintings">
    <h3>相关作品</h3>
    <div class="paintings-container">
      <div 
        v-for="painting in similarPaintings" 
        :key="painting.id"
        class="related-painting"
        @click="navigateToPainting(painting)"
      >
        <div class="painting-preview">
          <img :src="painting.thumbnail" :alt="painting.title">
          <div v-if="painting.isPremium" class="premium-indicator"></div>
        </div>
        <div class="painting-meta">
          <h4>{{ painting.title }}</h4>
          <p>{{ painting.artist }}</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'RelatedPaintings',
  props: {
    currentId: {
      type: String,
      required: true
    },
    similarPaintings: {
      type: Array,
      required: true
    }
  },
  methods: {
    navigateToPainting(painting) {
      if (painting.id === this.currentId) return
      this.$router.push({
        name: 'PaintingDetail',
        params: { 
          id: painting.id,
          isPremium: painting.isPremium
        }
      })
    }
  }
}
</script>

<style scoped>
.related-paintings {
  padding: 20px;
  background: rgba(255, 255, 255, 0.8);
  border-radius: 8px;
}

.paintings-container {
  display: flex;
  gap: 20px;
  overflow-x: auto;
  padding: 10px 0;
}

.related-painting {
  flex: 0 0 200px;
  cursor: pointer;
  transition: transform 0.3s;
}

.related-painting:hover {
  transform: translateY(-5px);
}

.painting-preview {
  position: relative;
  height: 150px;
  overflow: hidden;
  border-radius: 8px;
}

.painting-preview img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.premium-indicator {
  position: absolute;
  top: 5px;
  right: 5px;
  width: 10px;
  height: 10px;
  background: #ffd700;
  border-radius: 50%;
  box-shadow: 0 0 5px rgba(255, 215, 0, 0.5);
}

.painting-meta {
  padding: 10px 0;
}

.painting-meta h4 {
  margin: 0;
  font-size: 14px;
  color: #2c3e50;
}

.painting-meta p {
  margin: 5px 0 0;
  font-size: 12px;
  color: #666;
}
</style> 