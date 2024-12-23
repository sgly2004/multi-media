<template>
  <div class="timeline-cloud">
    <div class="debug-info">
      Dynasty: {{ dynasty }}, Words: {{ cloudWords.length }}
    </div>
    
    <!-- 添加朝代选择器 -->
    <div class="dynasty-selector">
      <select v-model="selectedDynasty">
        <option v-for="d in availableDynasties" 
                :key="d" 
                :value="d">{{ d }}</option>
      </select>
    </div>
    
    <svg ref="cloudContainer" width="100%" height="500">
      <g :transform="transform">
        <text v-for="word in cloudWords"
              :key="word.text"
              :x="word.x"
              :y="word.y"
              :font-size="word.size"
              :fill="getColor(word)"
              :style="{ fontFamily: 'KaiTi, serif' }"
              :class="'cloud-word'"
              text-anchor="middle"
              @click="$emit('wordClicked', word.text)">
          {{ word.text }}
        </text>
      </g>
    </svg>
  </div>
</template>

<script>
import { mockCloudWords } from '../mock_data/cloudWords'

export default {
  name: 'TimelineCloud',
  props: {
    dynasty: {
      type: String,
      required: true
    }
  },
  data() {
    return {
      transform: 'translate(300,200)',
      selectedDynasty: this.dynasty
    }
  },
  computed: {
    availableDynasties() {
      return Object.keys(mockCloudWords)
    },
    cloudWords() {
      console.log('当前朝代:', this.selectedDynasty);
      const dynastyWords = mockCloudWords[this.selectedDynasty] || [];
      
      if (dynastyWords.length === 0) {
        console.warn('警告: 未找到当前朝代的词云数据');
        return [];
      }
      
      // 按权重排序，确保大的词先放置
      const sortedWords = [...dynastyWords].sort((a, b) => b.size - a.size);
      const placedWords = [];
      
      for (const word of sortedWords) {
        const wordData = {
          text: word.text,
          size: this.calculateFontSize(word.size * 10),
          x: 0,
          y: 0,
          weight: word.size * 10
        };
        
        if (this.findValidPosition(wordData, placedWords)) {
          placedWords.push(wordData);
        }
      }
      
      return placedWords;
    }
  },
  methods: {
    calculateFontSize(weight) {
      const size = Math.max(16, Math.min(60, weight * 0.8))
      console.log(`计算字体大小: weight=${weight}, size=${size}`)
      return size
    },
    getColor(word) {
      const opacity = Math.max(0.3, Math.min(0.9, word.weight / 100))
      return `rgba(0, 0, 0, ${opacity})`
    },
    updateDimensions() {
      if (this.$refs.cloudContainer) {
        const bbox = this.$refs.cloudContainer.getBoundingClientRect()
        console.log('SVG容器尺寸:', bbox)
        // 更新transform以居中显示
        this.transform = `translate(${bbox.width/2},${bbox.height/2})`
      }
    },
    checkCollision(word1, word2) {
      const padding = 5; // 词之间的最小间距
      const w1 = word1.text.length * (word1.size / 2);
      const h1 = word1.size;
      const w2 = word2.text.length * (word2.size / 2);
      const h2 = word2.size;

      return Math.abs(word1.x - word2.x) < (w1 + w2) / 2 + padding &&
             Math.abs(word1.y - word2.y) < (h1 + h2) / 2 + padding;
    },

    findValidPosition(word, placedWords) {
      const maxAttempts = 100;
      const maxRadius = 200; // 最大分布半径
      
      for (let attempt = 0; attempt < maxAttempts; attempt++) {
        // 使用极坐标系统，确保词云围绕中心分布
        const angle = Math.random() * 2 * Math.PI;
        const radius = Math.sqrt(Math.random()) * maxRadius * (1 - attempt / maxAttempts);
        
        word.x = radius * Math.cos(angle);
        word.y = radius * Math.sin(angle);

        // 检查是否与已放置的词有重叠
        let hasCollision = false;
        for (const placedWord of placedWords) {
          if (this.checkCollision(word, placedWord)) {
            hasCollision = true;
            break;
          }
        }

        if (!hasCollision) {
          return true;
        }
      }
      return false;
    }
  },
  watch: {
    dynasty: {
      immediate: true,
      handler(newDynasty) {
        console.log('朝代改变:', newDynasty)
        this.selectedDynasty = newDynasty
      }
    }
  },
  mounted() {
    console.log('TimelineCloud mounted')
    this.updateDimensions()
    window.addEventListener('resize', this.updateDimensions)
  },
  beforeDestroy() {
    window.removeEventListener('resize', this.updateDimensions)
  }
}
</script>

<style scoped>
.timeline-cloud {
  padding: 20px;
  background: rgba(255, 255, 255, 0.8);
  border-radius: 8px;
  height: 500px;
  position: relative;
}

.dynasty-selector {
  position: absolute;
  top: 10px;
  right: 10px;
  z-index: 100;
}

.dynasty-selector select {
  padding: 5px;
  border-radius: 4px;
  border: 1px solid #ddd;
}

.debug-info {
  position: absolute;
  top: 0;
  left: 0;
  background: rgba(0,0,0,0.1);
  padding: 5px;
  font-size: 12px;
  z-index: 100;
}

.cloud-word {
  cursor: pointer;
  transition: transform 0.3s ease, fill 0.3s ease;
}

.cloud-word:hover {
  fill: #8b0000 !important;
  transform: scale(1.1) translateZ(0);
}

svg {
  border: 1px dashed rgba(0,0,0,0.1);
}
</style> 