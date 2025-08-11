import {createRouter, createWebHashHistory} from 'vue-router'
import login from '../views/login/login.vue'
import frame from '../views/main/frame.vue'
import {useAuthStore} from '@/stores/auth';
import myabsent from '@/views/absent/my.vue'
import subabsent from '@/views/absent/sub.vue'
import publish from '@/views/inform/publish.vue'
import inform_list from '@/views/inform/list.vue'
import detail from '@/views/inform/detail.vue'

const router = createRouter({
    history: createWebHashHistory(import.meta.env.BASE_URL),
    routes: [
        {
            path: '/',
            name: 'frame',
            component: frame,
            children: [
                {path: '/absent/my', name: 'myabsent', component: myabsent},
                {path: '/absent/sub', name: 'subabsent', component: subabsent},
                {path:'/inform/publish', name:'inform_publish',component: publish},
                {path:'/inform/list', name:'inform_list',component: inform_list},
                {path:'/inform/detail/:pk', name:'inform_detail',component: detail},

            ]
        },
        {
            path: '/login',
            name: 'login',
            component: login
        }
    ]
})

router.beforeEach((to, from) => {
    const authStore = useAuthStore();
    if (!authStore.is_logined && to.name != 'login') {
        return {name: 'login'}
    }
})

export default router
