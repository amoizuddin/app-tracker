import { createRouter, createWebHistory, RouteRecordRaw } from "vue-router";

const routes: Array<RouteRecordRaw> = [
  {
    path: "/",
    name: "dashboard",
    component: () => import("../views/DashboardPage.vue"),
  },
  {
    path: "/add",
    name: "AddApplication",
    component: () => import("../views/AddApplicationPage.vue"),
  },
  {
    path: "/edit/:id",
    name: "EditApplication",
    component: () => import("../views/EditApplicationPage.vue"),
  },
];

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes,
});

export default router;
