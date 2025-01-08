import { createRouter, createWebHistory } from 'vue-router'
import HomePage from '../components/HomePage.vue'
import PaintingDetail from '../components/PaintingDetail.vue'
import BackgroundSelect from '../components/BackgroundSelect.vue'
import CreateCanvas from '../components/CreateCanvas.vue'

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
  },
  {
    path: '/background-select',
    name: 'BackgroundSelect',
    component: BackgroundSelect
  },
  {
    path: '/create/:backgroundId',
    name: 'CreateCanvas',
    component: CreateCanvas,
    props: true
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router 