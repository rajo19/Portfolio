import { createRouter, createWebHistory } from 'vue-router';
import { useAuthStore } from '../stores/auth';

// Use dynamic imports for better code splitting
const HomeView = () => import('@/views/HomeView.vue');
const PortfolioView = () => import('@/views/PortfolioView.vue');
const CVView = () => import('@/views/CVView.vue');
const AIView = () => import('@/views/AIView.vue');
const BlogView = () => import('@/views/BlogView.vue');
const BlogPostView = () => import('@/views/BlogPostView.vue');
const BlogEditorView = () => import('@/views/BlogEditorView.vue');
const ContactView = () => import('@/views/ContactView.vue');
const AboutView = () => import('@/views/AboutView.vue');
const LoginView = () => import('@/views/LoginView.vue');
const ProfileManagementView = () => import('@/views/ProfileManagementView.vue');

const routes = [
  {
    path: '/',
    name: 'home',
    component: HomeView,
    meta: { title: 'Home' }
  },
  {
    path: '/portfolio',
    name: 'portfolio',
    component: PortfolioView,
    meta: { title: 'Portfolio' }
  },
  {
    path: '/cv',
    name: 'cv',
    component: CVView,
    meta: { title: 'CV' }
  },
  {
    path: '/ai',
    name: 'ai',
    component: AIView,
    meta: { title: 'AI Assistant' }
  },
  {
    path: '/blog',
    name: 'blog',
    component: BlogView,
    meta: { title: 'Blog' }
  },
  {
    path: '/blog/new',
    name: 'blog-new',
    component: BlogEditorView,
    meta: { title: 'New Post', requiresAuth: true }
  },
  {
    path: '/blog/:id',
    name: 'blog-post',
    component: BlogPostView,
    meta: { title: 'Blog Post' },
    props: true
  },
  {
    path: '/blog/:id/edit',
    name: 'blog-edit',
    component: BlogEditorView,
    meta: { title: 'Edit Post', requiresAuth: true },
    props: true
  },
  {
    path: '/contact',
    name: 'contact',
    component: ContactView,
    meta: { title: 'Contact' }
  },
  {
    path: '/about',
    name: 'about',
    component: AboutView,
    meta: { title: 'About' }
  },
  {
    path: '/login',
    name: 'login',
    component: LoginView,
    meta: { title: 'Login', guest: true }
  },
  {
    path: '/profile-management',
    name: 'profile-management',
    component: ProfileManagementView,
    meta: { title: 'Profile Management', requiresAuth: true }
  },
  {
    path: '/:pathMatch(.*)*',
    redirect: '/'
  }
]

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes,
  scrollBehavior(to, from, savedPosition) {
    if (savedPosition) {
      return savedPosition;
    } else if (to.hash) {
      return {
        el: to.hash,
        behavior: 'smooth',
        top: 100 // Offset for fixed header
      };
    } else {
      return { top: 0, behavior: 'smooth' };
    }
  }
});

// Navigation guard for protected routes
router.beforeEach(async (to, from, next) => {
  const authStore = useAuthStore();
  
  // Initialize auth state if not already done
  if (!authStore.isInitialized) {
    await authStore.init();
  }
  
  // Set page title
  document.title = to.meta.title ? `${to.meta.title} | Rajorshi Tah` : 'Rajorshi Tah';
  
  // Check if route requires authentication
  const requiresAuth = to.matched.some(record => record.meta.requiresAuth);
  const isGuestRoute = to.matched.some(record => record.meta.guest);
  
  // Handle authentication required routes
  if (requiresAuth && !authStore.isAuthenticated) {
    return next({
      path: '/login',
      query: { redirect: to.fullPath !== '/' ? to.fullPath : undefined }
    });
  }
  
  // Redirect authenticated users away from guest-only routes
  if (isGuestRoute && authStore.isAuthenticated) {
    return next(from.path === '/' ? '/dashboard' : from.path);
  }
  
  next();
});

export default router
