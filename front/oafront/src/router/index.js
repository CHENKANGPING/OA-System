import {createRouter, createWebHashHistory} from 'vue-router'
import {useAuthStore} from '@/stores/auth';
import frame_routes from "@/router/frame.js"
import login_routes from "@/router/login.js"

const router = createRouter({
    history: createWebHashHistory(import.meta.env.BASE_URL),
    routes: frame_routes.concat(login_routes)
})

router.beforeEach((to, from) => {
    const authStore = useAuthStore();
    if (!authStore.is_logined && to.name != 'login') {
        return {name: 'login'}
    }
})

export default router
