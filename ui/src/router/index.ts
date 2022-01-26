import {createRouter, createWebHashHistory, RouteRecordRaw} from "vue-router";
import Home from "@/views/Home.vue";
import SetupView from "@/views/SetupView.vue";
import store, {DeviceStatus} from "@/store"

const routes: Array<RouteRecordRaw> = [
    {
        path: '/',
        name: 'setup',
        component: SetupView
    },
    {
        path:"/device",
        name:"home",
        component:Home
    }
]


const router = createRouter({
    // 4. Provide the history implementation to use. We are using the hash history for simplicity here.
    history: createWebHashHistory(),
    routes, // short for `routes: routes`

})
router.beforeEach((to, from, next)=>{
    if(to.name=="setup"){
        next()
    }else {
        if (store.state.deviceStatus==DeviceStatus.NOT_CONNECTED){
            next({name:"setup"})
        }else {
            next()
        }
    }
})
export default router
