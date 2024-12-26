<template>
  <div class="create-canvas">
    <div class="toolbar">
      <button @click="exportCanvas">导出作品</button>
      <button v-if="selectedObjectIndex !== -1" @click="deleteSelected">删除</button>
    </div>

    <div class="canvas-container" 
      @drop="handleDrop" 
      @dragover.prevent
      ref="canvasContainer"
    >
      <img :src="backgroundUrl" class="background">
      
      <!-- 画布上的对象 -->
      <div 
        v-for="(obj, index) in canvasObjects" 
        :key="obj.id"
        class="canvas-object"
        :class="{ selected: selectedObjectIndex === index }"
        :style="{
          left: obj.x + 'px',
          top: obj.y + 'px',
          transform: `rotate(${obj.rotation}deg) scale(${obj.scale})`
        }"
        @mousedown="startDrag($event, index)"
        @click.stop="selectObject(index)"
      >
        <img :src="obj.url" :alt="obj.name">
        
        <!-- 控制点 - 仅在选中时显示 -->
        <template v-if="selectedObjectIndex === index">
          <!-- 旋转控制点 -->
          <div class="rotate-handle" @mousedown.stop="startRotate($event, index)"></div>
          
          <!-- 缩放控制点 -->
          <div class="scale-handle" @mousedown.stop="startScale($event, index)"></div>
        </template>
      </div>
    </div>
    
    <div class="object-selector">
      <div class="category-tabs">
        <button 
          v-for="category in categories" 
          :key="category"
          :class="{ active: currentCategory === category }"
          @click="loadCategoryObjects(category)"
        >
          {{ category }}
        </button>
      </div>
      
      <div class="objects-list">
        <div v-if="loading" class="loading">
          加载中...
        </div>
        <template v-else>
          <div 
            v-for="obj in currentObjects" 
            :key="obj.id"
            class="object-item"
            draggable="true"
            @dragstart="handleDragStart($event, obj)"
          >
            <img 
              :src="obj.url" 
              :alt="obj.name"
              @error="handleImageError(obj)"
            >
          </div>
        </template>
      </div>
    </div>
  </div>
</template>

<script>
import html2canvas from 'html2canvas';

export default {
  name: 'CreateCanvas',
  data() {
    return {
      backgroundUrl: '',
      categories: [],
      currentCategory: '',
      objects: {},
      currentObjects: [],
      loading: false,
      objectPaths: {},
      canvasObjects: [], // 画布上的对象
      selectedObjectIndex: -1, // 当前选中的对象索引
      isDragging: false,
      dragStartX: 0,
      dragStartY: 0,
      objectStartX: 0,
      objectStartY: 0,
      isRotating: false,
      isScaling: false,
      centerX: 0,
      centerY: 0,
      initialAngle: 0,
      initialScale: 1,
      initialDistance: 0
    }
  },
  methods: {
    async loadCategories() {
      try {
        console.log('开始加载类别...');
        
        // 只获取文件路径,不立即加载文件
        const modules = import.meta.glob('../assets/create/object/**/*.{png,jpg,jpeg}');
        console.log('找到的模块路径:', Object.keys(modules));
        
        // 初始化类别映射
        const categoryMap = {};
        
        // 处理每个文件路径
        Object.keys(modules).forEach(path => {
          console.log('处理路径:', path);
          
          // 从路径中提取类别和名称
          const parts = path.split('/');
          const category = parts[parts.length - 2];
          const name = parts[parts.length - 1].split('.')[0];
          
          // 保存文件路径映射
          if (!this.objectPaths[category]) {
            this.objectPaths[category] = {};
          }
          this.objectPaths[category][name] = modules[path];
          
          // 收集类别
          if (!categoryMap[category]) {
            categoryMap[category] = true;
            this.categories.push(category);
            console.log('添加新类别:', category);
          }
        });
        
        console.log('类别加载完成:', {
          类别数: this.categories.length,
          类别列表: this.categories
        });
        
      } catch (err) {
        console.error('加载类别失败:', err);
      }
    },
    
    async loadCategoryObjects(category) {
      try {
        console.log('加载类别对象:', category);
        this.loading = true;
        this.currentCategory = category;
        
        if (!this.objects[category]) {
          console.log('首次加载该类别对象');
          const categoryObjects = [];
          
          // 加载该类别下的所有图片
          for (const [name, importFn] of Object.entries(this.objectPaths[category])) {
            try {
              const module = await importFn();
              categoryObjects.push({
                id: `${category}-${name}`,
                name,
                url: module.default,
                category
              });
              console.log(`已加载对象: ${name}`);
            } catch (err) {
              console.error(`加载对象失败: ${name}`, err);
            }
          }
          
          this.objects[category] = categoryObjects;
        } else {
          console.log('使用缓存的类别对象');
        }
        
        this.currentObjects = this.objects[category] || [];
        console.log('当前类别对象数量:', this.currentObjects.length);
        
      } catch (err) {
        console.error('加载类别对象失败:', err);
      } finally {
        this.loading = false;
      }
    },
    
    addObjectToCanvas(obj) {
      console.log('添加对象到画布:', obj);
    },
    
    handleImageError(obj) {
      console.error('图片加载失败:', obj);
    },

    // 拖拽相关方法
    handleDragStart(event, obj) {
      event.dataTransfer.setData('text/plain', JSON.stringify(obj));
      event.dataTransfer.effectAllowed = 'copy';
    },

    handleDrop(event) {
      const obj = JSON.parse(event.dataTransfer.getData('text/plain'));
      const rect = event.currentTarget.getBoundingClientRect();
      const x = event.clientX - rect.left;
      const y = event.clientY - rect.top;
      
      this.canvasObjects.push({
        ...obj,
        x,
        y,
        scale: 1,
        rotation: 0 // 添加旋转属性
      });
    },

    startDrag(event, index) {
      if (event.button !== 0) return; // 只响应左键
      
      this.isDragging = true;
      this.selectedObjectIndex = index;
      
      const obj = this.canvasObjects[index];
      this.dragStartX = event.clientX;
      this.dragStartY = event.clientY;
      this.objectStartX = obj.x;
      this.objectStartY = obj.y;
      
      document.addEventListener('mousemove', this.handleDrag);
      document.addEventListener('mouseup', this.stopDrag);
    },

    handleDrag(event) {
      if (!this.isDragging) return;
      
      const deltaX = event.clientX - this.dragStartX;
      const deltaY = event.clientY - this.dragStartY;
      
      const obj = this.canvasObjects[this.selectedObjectIndex];
      obj.x = this.objectStartX + deltaX;
      obj.y = this.objectStartY + deltaY;
    },

    stopDrag() {
      this.isDragging = false;
      document.removeEventListener('mousemove', this.handleDrag);
      document.removeEventListener('mouseup', this.stopDrag);
    },

    selectObject(index) {
      this.selectedObjectIndex = index;
    },

    // 点击画布空白处取消选择
    handleCanvasClick(event) {
      if (event.target.classList.contains('canvas-container')) {
        this.selectedObjectIndex = -1;
      }
    },

    // 旋转相关方法
    startRotate(event, index) {
      event.stopPropagation();
      this.isRotating = true;
      this.selectedObjectIndex = index;
      
      const obj = this.canvasObjects[index];
      const rect = event.target.parentElement.getBoundingClientRect();
      
      this.centerX = rect.left + rect.width / 2;
      this.centerY = rect.top + rect.height / 2;
      this.initialAngle = obj.rotation || 0;
      
      const angle = Math.atan2(
        event.clientY - this.centerY,
        event.clientX - this.centerX
      ) * 180 / Math.PI;
      
      this.startAngle = angle - this.initialAngle;
      
      document.addEventListener('mousemove', this.handleRotate);
      document.addEventListener('mouseup', this.stopRotate);
    },

    handleRotate(event) {
      if (!this.isRotating) return;
      
      const angle = Math.atan2(
        event.clientY - this.centerY,
        event.clientX - this.centerX
      ) * 180 / Math.PI;
      
      const newRotation = angle - this.startAngle;
      this.canvasObjects[this.selectedObjectIndex].rotation = newRotation;
    },

    stopRotate() {
      this.isRotating = false;
      document.removeEventListener('mousemove', this.handleRotate);
      document.removeEventListener('mouseup', this.stopRotate);
    },

    // 缩放相关方法
    startScale(event, index) {
      event.stopPropagation();
      this.isScaling = true;
      this.selectedObjectIndex = index;
      
      const obj = this.canvasObjects[index];
      const rect = event.target.parentElement.getBoundingClientRect();
      
      this.centerX = rect.left + rect.width / 2;
      this.centerY = rect.top + rect.height / 2;
      this.initialScale = obj.scale || 1;
      this.initialDistance = Math.hypot(
        event.clientX - this.centerX,
        event.clientY - this.centerY
      );
      
      document.addEventListener('mousemove', this.handleScale);
      document.addEventListener('mouseup', this.stopScale);
    },

    handleScale(event) {
      if (!this.isScaling) return;
      
      const currentDistance = Math.hypot(
        event.clientX - this.centerX,
        event.clientY - this.centerY
      );
      
      const scaleFactor = currentDistance / this.initialDistance;
      const newScale = this.initialScale * scaleFactor;
      
      // 限制缩放范围
      if (newScale >= 0.2 && newScale <= 3) {
        this.canvasObjects[this.selectedObjectIndex].scale = newScale;
      }
    },

    stopScale() {
      this.isScaling = false;
      document.removeEventListener('mousemove', this.handleScale);
      document.removeEventListener('mouseup', this.stopScale);
    },

    // 删除选中对象
    deleteSelected() {
      if (this.selectedObjectIndex !== -1) {
        this.canvasObjects.splice(this.selectedObjectIndex, 1);
        this.selectedObjectIndex = -1;
      }
    },

    // 导出画布
    async exportCanvas() {
      try {
        const canvas = await html2canvas(this.$refs.canvasContainer, {
          useCORS: true, // 允许跨域图片
          scale: 2 // 提高导出质量
        });
        
        // 创建下载链接
        const link = document.createElement('a');
        link.download = '我的创作.png';
        link.href = canvas.toDataURL('image/png');
        link.click();
      } catch (err) {
        console.error('导出失败:', err);
        alert('导出失败，请重试');
      }
    }
  },
  created() {
    console.log('CreateCanvas组件创建');
    this.backgroundUrl = this.$route.query.bgUrl;
    console.log('背景图片URL:', this.backgroundUrl);
  },
  async mounted() {
    console.log('CreateCanvas组件挂载');
    await this.loadCategories();
    
    // 如果有类别,加载第一个类别的对象
    if (this.categories.length > 0) {
      await this.loadCategoryObjects(this.categories[0]);
    }
    document.addEventListener('click', this.handleCanvasClick);
  },
  beforeUnmount() {
    document.removeEventListener('click', this.handleCanvasClick);
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
  user-select: none; /* 防止拖拽时选中文本 */
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

.loading {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #666;
  font-size: 1.1rem;
  font-family: "KaiTi", serif;
}

.canvas-object {
  position: absolute;
  cursor: move;
  transition: none; /* 移除过渡效果以实现平滑的拖拽 */
}

.canvas-object.selected {
  outline: 2px solid #8b0000;
  outline-offset: 2px;
  z-index: 1;
}

.canvas-object img {
  pointer-events: none; /* 防止图片干扰拖拽 */
  max-width: 100px; /* 限制初始大小 */
  height: auto;
}

.object-item {
  cursor: grab;
}

.object-item:active {
  cursor: grabbing;
}

.toolbar {
  padding: 10px;
  background: white;
  border-bottom: 1px solid #ddd;
  display: flex;
  gap: 10px;
}

.toolbar button {
  padding: 8px 16px;
  background: #8b0000;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-family: "KaiTi", serif;
  transition: all 0.3s;
}

.toolbar button:hover {
  background: #a00000;
}

/* 旋转控制点 */
.rotate-handle {
  position: absolute;
  width: 20px;
  height: 20px;
  background: #8b0000;
  border-radius: 50%;
  top: -30px;
  left: 50%;
  transform: translateX(-50%);
  cursor: pointer;
}

.rotate-handle::after {
  content: '';
  position: absolute;
  width: 2px;
  height: 10px;
  background: #8b0000;
  left: 50%;
  bottom: 100%;
  transform: translateX(-50%);
}

/* 缩放控制点 */
.scale-handle {
  position: absolute;
  width: 20px;
  height: 20px;
  background: #8b0000;
  border-radius: 50%;
  bottom: -10px;
  right: -10px;
  cursor: se-resize;
}
</style> 