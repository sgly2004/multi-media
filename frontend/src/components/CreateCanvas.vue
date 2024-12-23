<template>
  <div class="create-canvas">
    <div class="canvas-container">
      <img :src="backgroundUrl" class="background">
      <!-- 这里将添加可拖拽的元素 -->
    </div>
    
    <div class="object-selector">
      <div class="category-tabs">
        <button 
          v-for="category in categories" 
          :key="category"
          :class="{ active: currentCategory === category }"
          @click="currentCategory = category"
        >
          {{ category }}
        </button>
      </div>
      
      <div class="objects-list">
        <div 
          v-for="obj in currentObjects" 
          :key="obj.id"
          class="object-item"
          @click="addObjectToCanvas(obj)"
        >
          <img :src="obj.url" :alt="obj.name">
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'CreateCanvas',
  data() {
    return {
      backgroundUrl: '',
      categories: [],
      currentCategory: '',
      objects: {},
      currentObjects: []
    }
  },
  methods: {
    async loadObjects() {
      try {
        console.log('开始加载对象元素...');
        
        // 使用 Vite 的 import.meta.glob 加载所有对象文件
        const modules = import.meta.glob('../assets/create/object/**/*.{png,jpg,jpeg}', { eager: true });
        console.log('找到的模块:', modules);
        
        const objects = {};
        
        // 处理每个文件路径
        Object.entries(modules).forEach(([path, module]) => {
          console.log('处理文件:', path);
          
          // 从路径中提取类别和名称
          const parts = path.split('/');
          const category = parts[parts.length - 2];
          const name = parts[parts.length - 1].split('.')[0];
          
          console.log('解析结果:', {
            类别: category,
            名称: name,
            完整路径: path
          });
          
          // 初始化类别数组
          if (!objects[category]) {
            objects[category] = [];
            this.categories.push(category);
            console.log('添加新类别:', category);
          }
          
          // 添加对象到对应类别
          objects[category].push({
            id: `${category}-${name}`,
            name: name,
            url: module.default,
            category: category
          });
          
          console.log(`已将 ${name} 添加到 ${category} 类别`);
        });
        
        this.objects = objects;
        console.log('对象加载完成:', {
          类别数量: this.categories.length,
          类别列表: this.categories,
          对象总数: Object.values(objects).flat().length
        });
        
        // 设置默认类别
        if (this.categories.length > 0) {
          this.currentCategory = this.categories[0];
          console.log('设置默认类别:', this.currentCategory);
        }
      } catch (err) {
        console.error('加载对象元素失败:', err);
      }
    },
    addObjectToCanvas(obj) {
      console.log('添加对象到画布:', obj);
    }
  },
  watch: {
    currentCategory: {
      immediate: true,
      handler(category) {
        console.log('切换类别:', category);
        this.currentObjects = this.objects[category] || [];
        console.log('当前类别的对象数量:', this.currentObjects.length);
      }
    }
  },
  created() {
    console.log('CreateCanvas组件创建');
    this.backgroundUrl = this.$route.query.bgUrl;
    console.log('背景图片URL:', this.backgroundUrl);
  },
  mounted() {
    console.log('CreateCanvas组件挂载');
    this.loadObjects();
  }
}
</script>

<style scoped>
.create-canvas {
  height: 100vh;
  display: flex;
  flex-direction: column;
}

.canvas-container {
  flex: 1;
  position: relative;
  overflow: hidden;
  background: #f0f0f0;
}

.background {
  width: 100%;
  height: 100%;
  object-fit: contain;
}

.object-selector {
  height: 150px;
  background: white;
  border-top: 1px solid #ddd;
  padding: 10px;
  display: flex;
  flex-direction: column;
}

.category-tabs {
  display: flex;
  gap: 10px;
  margin-bottom: 10px;
  padding: 0 10px;
  overflow-x: auto;
  scrollbar-width: thin;
}

.category-tabs button {
  padding: 5px 15px;
  border: none;
  background: #f0f0f0;
  cursor: pointer;
  border-radius: 4px;
  white-space: nowrap;
  font-family: "KaiTi", serif;
}

.category-tabs button.active {
  background: #8b0000;
  color: white;
}

.objects-list {
  display: flex;
  gap: 10px;
  overflow-x: auto;
  padding: 10px;
  flex: 1;
  scrollbar-width: thin;
}

.object-item {
  flex: 0 0 80px;
  height: 80px;
  cursor: pointer;
  border: 1px solid #ddd;
  border-radius: 4px;
  overflow: hidden;
  transition: all 0.3s ease;
}

.object-item:hover {
  border-color: #8b0000;
  transform: translateY(-2px);
}

.object-item img {
  width: 100%;
  height: 100%;
  object-fit: contain;
}

/* 自定义滚动条样式 */
.category-tabs::-webkit-scrollbar,
.objects-list::-webkit-scrollbar {
  height: 6px;
}

.category-tabs::-webkit-scrollbar-track,
.objects-list::-webkit-scrollbar-track {
  background: #f0f0f0;
}

.category-tabs::-webkit-scrollbar-thumb,
.objects-list::-webkit-scrollbar-thumb {
  background: #ddd;
  border-radius: 3px;
}

.category-tabs::-webkit-scrollbar-thumb:hover,
.objects-list::-webkit-scrollbar-thumb:hover {
  background: #ccc;
}
</style> 