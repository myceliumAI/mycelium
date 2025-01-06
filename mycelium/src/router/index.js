import { createRouter, createWebHistory } from 'vue-router'
import { authService } from '@/services/auth.service'
import Home from '@/views/home/Home.vue'
import Login from '@/views/auth/Login.vue'
import Register from '@/views/auth/Register.vue'

const routes = [
  {
    path: '/',
    name: 'Home',
    component: Home,
    meta: { requiresAuth: true }
  },
  {
    path: '/login',
    name: 'Login',
    component: Login,
    meta: { requiresUnauth: true }
  },
  {
    path: '/register',
    name: 'Register',
    component: Register,
    meta: { requiresUnauth: true }
  },
  {
    path: '/silent-check-sso',
    name: 'SilentCheckSso',
    component: () => import('@/views/auth/SilentCheckSso.vue')
  }
]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})

router.beforeEach(async (to, from, next) => {
  try {
    const isAuthenticated = authService.isAuthenticated.value

    if (to.meta.requiresAuth && !isAuthenticated) {
      console.log('⚠️ Authentication required, redirecting to login')
      return next('/login')
    }

    if (to.meta.requiresUnauth && isAuthenticated) {
      console.log('⚠️ Already authenticated, redirecting to home')
      return next('/')
    }

    next()
  } catch (error) {
    console.error('❌ Navigation error:', error)
    next('/login')
  }
})

export default router
