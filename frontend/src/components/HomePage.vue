<template>
  <div class="home-container">
    <div class="scroll-outer">
      <div class="scroll-container">
        <div class="scroll-content">
          <transition name="fade">
            <TimelineCloud 
              v-if="!showGallery"
              :dynasty="currentDynasty"
              @wordClicked="handleWordClick"
            />
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
      paintings: mockPaintings
    }
  },
  computed: {
    currentDynasty() {
      console.log('Current dynasty:', this.dynasties[this.dynastyIndex])
      return this.dynasties[this.dynastyIndex]
    },
    filteredPaintings() {
      console.log('Filtering paintings for dynasty:', this.currentDynasty);
      console.log('Selected word:', this.selectedWord);
      console.log('All paintings:', this.paintings);
      
      if (!this.selectedWord) {
        return this.paintings.filter(p => p.dynasty === this.currentDynasty);
      }
      
      const filtered = this.paintings.filter(p => 
        p.dynasty === this.currentDynasty && 
        p.tags.includes(this.selectedWord)
      );
      
      console.log('Filtered paintings:', filtered);
      return filtered;
    }
  },
  methods: {
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
      console.log('Word clicked:', word)
      this.selectedWord = word
      this.showGallery = true
    },
    navigateToPainting(painting) {
      console.log('Navigating to painting:', painting)
      this.$router.push({
        name: 'PaintingDetail',
        params: { 
          id: painting.id
        }
      })
    },
    closeGallery() {
      this.showGallery = false;
      this.selectedWord = '';
    }
  },
  mounted() {
    console.log('HomePage mounted')
    console.log('Initial dynasty:', this.currentDynasty)
    console.log('Available dynasties:', this.dynasties)
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
</style> 