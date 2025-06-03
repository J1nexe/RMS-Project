import { createRouter, createWebHistory } from "vue-router";
import home from '../src/pages/Home.vue';
import data from '../src/pages/data.vue';
import Login from '../src/pages/Login.vue';
import Register from '../src/components/register.vue';

const routes = [
    {
        path: '/',
        redirect: '/login'
    },
    {
        path: '/login',
        name: 'Login',
        component: Login
    },
    {
        path: '/register',
        name: 'Register',
        component: Register
    },
    {
        path: '/home',
        name: 'Home',
        component: home,
        meta: { requiresAuth: true }
    },
    {
        path: '/data',
        name: 'Data',
        component: data,
        meta: { requiresAuth: true }
    }
];

const router = createRouter({
    history: createWebHistory(),
    routes
});

// Navigation guard for authentication
router.beforeEach((to, from, next) => {
    const user = localStorage.getItem('user');
    
    if (to.meta.requiresAuth && !user) {
        next('/login');
    } else if ((to.path === '/login' || to.path === '/register') && user) {
        next('/home');
    } else {
        next();
    }
});

export default router;