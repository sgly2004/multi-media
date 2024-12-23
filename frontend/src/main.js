import { createApp } from 'vue'
import { createRouter, createWebHistory } from 'vue-router'
import App from './App.vue'
import HomePage from './components/HomePage.vue'
import PaintingDetail from './components/PaintingDetail.vue'
import BackgroundSelect from './components/BackgroundSelect.vue'
import CreateCanvas from './components/CreateCanvas.vue'

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
    },
    {
      path: '/background-select',
      name: 'BackgroundSelect',
      component: BackgroundSelect,
      props: true
    },
    {
      path: '/create/:backgroundId',
      name: 'CreateCanvas',
      component: CreateCanvas,
      props: true
    }
  ]
})

const app = createApp(App)

app.config.errorHandler = (err) => {
  console.error('Application error:', err)
}

app.use(router)
app.mount('#app')
