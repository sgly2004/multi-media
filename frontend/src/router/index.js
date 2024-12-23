import { createRouter, createWebHistory } from 'vue-router'
import HomePage from '../components/HomePage.vue'
import PaintingDetail from '../components/PaintingDetail.vue'

const routes = [
  {
    path: '/',
    name: 'Home',
    component: HomePage
  },
  {
    path: '/painting/:id',
    name: 'PaintingDetail',
    component: PaintingDetail
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router 