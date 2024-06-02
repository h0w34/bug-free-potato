import {createRouter, createWebHistory} from 'vue-router'

import HomePage from '@/pages/Home.vue'
import CreatePage from '@/components/Create.vue'
import ProfilePage from '@/pages/Profile.vue'
import ArchivePage from '@/pages/Archive.vue'

const routes = [
    {
        path: '/',
        name: 'home',
        component: HomePage
    },
    {
        path: '/create',
        name: 'create',
        component: CreatePage
    },
    {
        path: '/profile',
        name: 'profile',
        component: ProfilePage
    },
    {
        path: '/archive',
        name: 'arhive',
        component: ArchivePage
    }
]

const router = createRouter({
    history: createWebHistory(),
    routes
})

export default router;