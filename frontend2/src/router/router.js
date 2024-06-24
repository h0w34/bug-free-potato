import {createRouter, createWebHistory} from 'vue-router'
import NavigationGuards from "@/router/NavigationGuards";

/*
import { useAuthStore } from '@/store/auth.store'
*/

import HomePage from '@/pages/Home.vue'
import CreatePage from '@/components/Create.vue'
import ProfilePage from '@/pages/Profile.vue'
import ArchivePage from '@/pages/Archive.vue'
import UserDataService from "@/services/user-data.service";
import NotFoundPage from "@/components/NotFoundPage";
import LoginPage from "@/pages/LoginPage";
import signUpPage from "@/pages/SignUpPage";
import ResourcesPage from "@/pages/Resources";
/*import store from "@/store";*/

const routes = [
    {
        path: '/',
        name: 'home',
        component: HomePage,
        meta: { requiresAuth: true, navbar: true, guest: false }
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
        meta: { requiresAuth: true, navbar: true, guest: true  },
        props: true,
        beforeEnter: async (to, from, next) => {
            try {
                // Check if the user exists
                console.log('username: ', to.params.username)
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
        path: '/resources',
        name: 'resources',
        component: ResourcesPage,
        meta: { requiresAuth: true, navbar: true, guest: false }
    },
    {
        path: '/:pathMatch(.*)*', // Catch-all route for 404 error
        name: 'not-found',
        component: NotFoundPage
    },

]

export const router = createRouter({
        history: createWebHistory(),
        routes
})

router.beforeEach(NavigationGuards.authGuard)
router.beforeEach(NavigationGuards.beforeLeaveGuard)
    /*beforeEach(to, from, next) {
    if (store.state.layoutStore.sidebar) {

      store.commit('layoutStore/closeSidebar');
    }
    next();
    }*/
    /*beforeEnter: (to, from, next) => {
      if (store.state.layoutStore.sidebar) {
        console.log('in here!');
        store.commit('layoutStore/closeSidebar');
      }
      next();
    }*/


/*router.beforeEach(async (to) => {
    // redirect to login page if not logged in and trying to access a restricted page
    const publicPages = ['/login'];
    const authRequired = !publicPages.includes(to.path);
    const auth = useAuthStore();

    if (authRequired && !auth.user) {
        auth.returnUrl = to.fullPath;
        return '/login';
    }
});*/

/*
router.beforeEach((to, from, next) => {
  if (to.matched.some((record) => record.meta.requiresAuth)) {
    if (!store.state.token) {
      next({ name: 'login' });
    } else {
      axios.get('http://localhost:5000/auth/verify', {
        headers: {
          Authorization: `Bearer ${store.state.token}`,
        },
      })
        .then(() => {
          next();
        })
        .catch((error) => {
          if (error.response.status === 401) {
            store.dispatch('logout');
            next({ name: 'login' });
          }
        });
    }
  } else {
    next();
  }
});*/
