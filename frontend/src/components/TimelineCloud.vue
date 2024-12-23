<template>
  <div class="timeline-cloud">
    <div class="debug-info">
      Dynasty: {{ dynasty }}, Words: {{ cloudWords.length }}
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
      transform: 'translate(300,200)'
    }
  },
  computed: {
    cloudWords() {
      console.log('Computing cloudWords for dynasty:', this.dynasty)
      // 从 mockCloudWords 获取当前朝代的词云数据
      const dynastyWords = mockCloudWords[this.dynasty] || []
      
      // 转换数据格式并添加位置信息
      const words = dynastyWords.map(word => ({
        text: word.text,
        size: this.calculateFontSize(word.size * 10), // 将原始 size 值放大
        x: Math.random() * 500,
        y: Math.random() * 300,
        weight: word.size * 10 // 将原始 size 值放大用于颜色计算
      }))
      
      console.log('Generated cloudWords:', words)
      return words
    }
  },
  methods: {
    calculateFontSize(weight) {
      return Math.max(16, Math.min(60, weight * 0.8))
    },
    getColor(word) {
      const opacity = Math.max(0.3, Math.min(0.9, word.weight / 100))
      return `rgba(0, 0, 0, ${opacity})`
    }
  },
  mounted() {
    console.log('TimelineCloud mounted, dynasty:', this.dynasty)
    console.log('Container size:', this.$refs.cloudContainer?.getBoundingClientRect())
  },
  updated() {
    console.log('TimelineCloud updated, dynasty:', this.dynasty)
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