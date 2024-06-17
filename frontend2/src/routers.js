import {createRouter, createWebHistory} from 'vue-router'

import HomePage from '@/pages/Home.vue'
import CreatePage from '@/components/Create.vue'
import ProfilePage from '@/pages/Profile.vue'
import ArchivePage from '@/pages/Archive.vue'
import UserDataService from "@/services/UserDataService";
import NotFoundPage from "@/components/NotFoundPage";
import LoginPage from "@/pages/LoginPage";
import signUpPage from "@/pages/SignUpPage";

const routes = [
    {
        path: '/',
        name: 'home',
        component: HomePage,
        meta: { requiresAuth: true, guest: false, navbar: true }
    },
    {
        path: '/create',
        name: 'create',
        component: CreatePage
    },
    {
        path: '/users/:username',
        name: 'user',
        component: ProfilePage,
        meta: { navbar: true },
        props: true,
         beforeEnter: async (to, from, next) => {
            try {
                // Check if the user exists
                const user = await UserDataService.getUserByUsername(to.params.username);
                if (!user) {
                    // If the user does not exist, redirect to the 404 error page
                    next({ name: 'not-found' });
                } else {
                    // If the user exists, continue with the route
                    next();
                }
            } catch (error) {
                // Handle any errors that occurred during the user lookup
                console.error(error);
                next({ name: 'not-found' });
            }
        }
    },
    {
        path: '/login',
        name: 'login',
        component: LoginPage,
        meta: { navbar: false }
    },
    {
        path: '/signup',
        name: 'signup',
        component: signUpPage,
        meta: { navbar: false }
    },
    {
        path: '/archive',
        name: 'arhive',
        component: ArchivePage
    },
    {
        path: '/:pathMatch(.*)*', // Catch-all route for 404 error
        name: 'not-found',
        component: NotFoundPage
    }
]

const router = createRouter({
    history: createWebHistory(),
    routes
})

export default router;