<template>
  <div class="timeline-cloud">
    <!-- <div class="debug-info">
      Dynasty: {{ dynasty }}, Words: {{ cloudWords.length }}
    </div> -->
    
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
      const size = Math.max(24, Math.min(80, weight * 1.5))
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
      const maxAttempts = 200; // 增加尝试次数
      const maxRadius = 550; // 增加最大半径
      
      // 优先考虑水平方向的分布
      for (let attempt = 0; attempt < maxAttempts; attempt++) {
        let x, y;
        
        if (attempt < maxAttempts / 2) {
          // 前一半的尝试更倾向于水平分布
          x = (Math.random() - 0.5) * maxRadius * 1.6; // 水平方向扩大1.5倍
          y = (Math.random() - 0.5) * maxRadius * 0.6; // 垂直方向稍微收缩
        } else {
          // 后一半的尝试使用极坐标系统
          const angle = Math.random() * 2 * Math.PI;
          const radius = Math.sqrt(Math.random()) * maxRadius;
          x = radius * Math.cos(angle);
          y = radius * Math.sin(angle);
        }
        
        word.x = x;
        word.y = y;

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
    },

    handleDynastySelect(dynasty) {
      this.selectedDynasty = dynasty;
      this.$emit('dynastyChange', dynasty);
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