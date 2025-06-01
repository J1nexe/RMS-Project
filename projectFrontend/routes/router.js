import { createRouter, createWebHistory } from "vue-router";
import home from '../src/pages/Home.vue';
// import login from '../src/pages/Login.vue';
import data from '../src/pages/data.vue';

const routes = [

    {
        path: '/',
        redirect: '/home'
    },
    {
        path: '/home',
        name: 'Home',
        component: home
    },
    // {
    //     path: '/login',
    //     name: 'Login',
    //     component: login
    // }
    {
        path: '/data',
        name: 'Data',
        component: data
    }
]

const router = createRouter({
    history: createWebHistory(),
    routes
})

export default router;