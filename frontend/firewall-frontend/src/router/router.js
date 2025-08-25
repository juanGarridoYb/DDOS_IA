import { createRouter, createWebHistory } from "vue-router";
import TrafficDashboard from "@/views/Dashboard.vue";

const routes = [
  {
    path: "/",
    name: "TrafficDashboard",
    component: TrafficDashboard,
  },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;
