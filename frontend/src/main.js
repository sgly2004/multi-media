import { createApp } from 'vue'
import { createRouter, createWebHistory } from 'vue-router'
import App from './App.vue'
import HomePage from './components/HomePage.vue'
import PaintingDetail from './components/PaintingDetail.vue'

console.log('Starting application...')

const router = createRouter({
  history: createWebHistory(),
  routes: [
    {
      path: '/',
      name: 'Home',
      component: HomePage
    },
    {
      path: '/painting/:id',
      name: 'PaintingDetail',
      component: PaintingDetail,
      props: true
    }
  ]
})

const app = createApp(App)

// 简单的错误处理
app.config.errorHandler = (err) => {
  console.error('Application error:', err)
}

app.use(router)
app.mount('#app')
