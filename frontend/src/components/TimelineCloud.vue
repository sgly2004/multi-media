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
      words: [
        { text: '山水', weight: 80 },
        { text: '人物', weight: 70 },
        { text: '花鸟', weight: 60 },
        { text: '走兽', weight: 50 },
        { text: '仕女', weight: 45 },
        { text: '佛像', weight: 40 }
      ]
    }
  },
  computed: {
    cloudWords() {
      console.log('Computing cloudWords for dynasty:', this.dynasty)
      const words = this.words.map(word => ({
        text: word.text,
        size: this.calculateFontSize(word.weight),
        x: Math.random() * 500,
        y: Math.random() * 300,
        weight: word.weight
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