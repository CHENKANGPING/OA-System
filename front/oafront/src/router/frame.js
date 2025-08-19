import frame from "../views/main/frame.vue";
import myabsent from "@/views/absent/my.vue";
import subabsent from "@/views/absent/sub.vue";
import publish from "@/views/inform/publish.vue";
import inform_list from "@/views/inform/list.vue";
import detail from "@/views/inform/detail.vue";
import staffadd from "@/views/staff/add.vue";
import stafflist from "@/views/staff/list.vue";
import home from "@/views/home/home.vue";
import absent from "@/views/absent/index.vue"
import inform from "@/views/inform/index.vue"
import staff from "@/views/staff/index.vue"

const routes = [
    {
        path: "/",
        name: "frame",
        component: frame,
        children: [
            {
                path: "/", name: "home", component: home,
                meta: {
                    icon: "HomeFilled",
                    text: "首页"
                },
            },
            {
                path: "/absent", name: "absent", component: absent,
                meta: {
                    icon: "Checked",
                    text: "考勤管理"
                },
                children: [
                    {
                        path: "/my", name: "myabsent", component: myabsent,
                        meta: {
                            icon: "UserFilled",
                            text: "个人考勤"
                        }
                    },
                    {
                        path: "/sub", name: "subabsent", component: subabsent,
                        meta: {
                            icon: "User",
                            text: "下属考勤"
                        },
                    },

                ]
            },
            {
                path: "/inform", name: "inform", component: inform,
                meta: {
                    icon: "BellFilled",
                    text: "通知管理"
                },
                children: [
                    {
                        path: "/publish", name: "inform_publish", component: publish,
                        meta: {
                            icon: "BellFilled",
                            text: "发布通知"
                        },
                    },
                    {
                        path: "/list", name: "inform_list", component: inform_list,
                        meta: {
                            icon: "Tickets",
                            text: "通知列表"
                        },
                    },
                    {path: "/detail/:pk", name: "inform_detail", component: detail},
                ]
            },
            {
                path: "/staff", name: staff, component: staff,
                meta: {
                    icon: "Avatar",
                    text: "员工管理"
                },
                children: [
                    {
                        path: "/add", name: "staff_add", component: staffadd,
                        meta: {
                            icon: "Plus",
                            text: "新增员工"
                        },
                    },
                    {
                        path: "/list", name: "staff_list", component: stafflist,
                        meta: {
                            icon: "Tickets",
                            text: "员工列表"
                        },
                    },

                ]
            },

        ],
    },
]

export default routes;
