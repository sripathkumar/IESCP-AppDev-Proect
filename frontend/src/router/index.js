import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../components/HomeView.vue'
import EditCampaign from '@/components/EditCampaign.vue';
import EditAd from '@/components/EditAd.vue';
import AddingAd from '@/components/AddingAd.vue'
import All_Ad from '@/components/All_Ad.vue';

const routes = [
  {
    path: '/',
    name: 'home',
    component: HomeView
  },
  {
    path: '/login',
    name: 'login',
    component: () => import(/* webpackChunkName: "about" */ '../components/login.vue')
  },
  {
    path: '/register-brand',
    name: 'register-brand',
    component: () => import(/* webpackChunkName: "about" */ '../components/register-brand.vue')
  },
  {
    path: '/register-influencer',
    name: 'register-influencer',
    component: () => import(/* webpackChunkName: "about" */ '../components/register-influencer.vue')
  },
  {
    path: '/sponsor-dashboard',
    name: 'sponsor-dashboard',
    component: () => import(/* webpackChunkName: "about" */ '../components/sponsor-dashboard.vue')
  },
  {
    path: '/Admin-dashboard',
    name: 'Admin-dashboard',
    component: () => import(/* webpackChunkName: "about" */ '../components/Admin-dashboard.vue')
  },
  {
    path: '/influencer-dashboard',
    name: 'influencer-dashboard',
    component: () => import(/* webpackChunkName: "about" */ '../components/influencer-dashboard.vue')
  },
  {
    path: '/edit-campaign/:id',
    name: 'EditCampaign',
    component: EditCampaign,
  },
  {
    path: '/edit-ad/:id',
    name: 'EditAd',
    component: EditAd,
  },
  {
    path: '/add-ad/:id',
    name: 'AddingAd',
    component: AddingAd,
  },
  {
    path: '/ads',
    name: 'Ads',
    component: All_Ad
  },
]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})

export default router
