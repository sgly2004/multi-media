<template>
  <div class="background-select">
    <div class="header">
      <h2>选择创作背景</h2>
      <button class="back-btn" @click="goBack">返回</button>
    </div>
    <div v-if="error" class="error-message">
      {{ error }}
    </div>
    <div v-else-if="loading" class="loading">
      加载中...
    </div>
    <div v-else class="backgrounds-grid">
      <div 
        v-for="bg in backgrounds" 
        :key="bg.id"
        class="background-item"
        @click="selectBackground(bg)"
      >
        <img :src="bg.url" :alt="bg.name">
        <p>{{ bg.name }}</p>
      </div>
    </div>
  </div>
</template>

<script>
import { defineComponent, ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'

export default defineComponent({
  name: 'BackgroundSelect',
  setup() {
    const router = useRouter()
    const backgrounds = ref([])
    const error = ref(null)
    const loading = ref(true)

    const loadBackgrounds = async () => {
      try {
        console.log('开始加载背景图片...')
        loading.value = true
        error.value = null

        // 使用相对路径
        const modules = import.meta.glob('/src/assets/create/background/*.{png,jpg,jpeg}', { eager: true })
        console.log('找到的模块:', modules)

        if (Object.keys(modules).length === 0) {
          throw new Error('没有找到任何背景图片')
        }

        backgrounds.value = Object.entries(modules).map(([path, module]) => {
          const name = path.split('/').pop().split('.')[0]
          return {
            id: name,
            name,
            url: module.default
          }
        })

        console.log('加载完成，背景数量:', backgrounds.value.length)
      } catch (err) {
        console.error('加载背景图片失败:', err)
        error.value = `加载背景图片失败: ${err.message}`
      } finally {
        loading.value = false
      }
    }

    const selectBackground = (bg) => {
      console.log('选择背景:', bg)
      router.push({
        name: 'CreateCanvas',
        params: { backgroundId: bg.id },
        query: { bgUrl: bg.url }
      })
    }

    const goBack = () => {
      router.push('/')
    }

    onMounted(() => {
      console.log('BackgroundSelect 组件已挂载')
      loadBackgrounds()
    })

    return {
      backgrounds,
      error,
      loading,
      selectBackground,
      goBack
    }
  }
})
</script>

<style scoped>
.background-select {
  min-height: 100vh;
  padding: 2rem;
  background: #f9f4e6;
}

.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 2rem;
  max-width: 1200px;
  margin: 0 auto 2rem;
}

h2 {
  text-align: center;
  color: #8b0000;
  font-family: "KaiTi", serif;
  font-size: 2rem;
  margin: 0;
}

.back-btn {
  padding: 0.5rem 1rem;
  background: #8b0000;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-family: "KaiTi", serif;
  transition: all 0.3s;
}

.back-btn:hover {
  background: #a00000;
}

.loading {
  text-align: center;
  padding: 2rem;
  font-size: 1.2rem;
  color: #666;
}

.error-message {
  color: #8b0000;
  text-align: center;
  padding: 2rem;
  font-size: 1.2rem;
  background: #fff;
  border-radius: 8px;
  margin: 2rem auto;
  max-width: 600px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
}

.backgrounds-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
  gap: 2rem;
  padding: 1rem;
  max-width: 1200px;
  margin: 0 auto;
}

.background-item {
  cursor: pointer;
  transition: all 0.3s ease;
  border-radius: 8px;
  overflow: hidden;
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
  background: white;
}

.background-item:hover {
  transform: translateY(-5px);
  box-shadow: 0 4px 12px rgba(0,0,0,0.2);
}

.background-item img {
  width: 100%;
  height: 200px;
  object-fit: cover;
  display: block;
}

.background-item p {
  padding: 1rem;
  text-align: center;
  margin: 0;
  font-family: "KaiTi", serif;
  color: #2c3e50;
  font-size: 1.1rem;
}
</style>