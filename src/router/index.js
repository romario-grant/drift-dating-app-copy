import { createRouter, createWebHistory } from "vue-router";
import HomeView from "../views/HomeView.vue";

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: "/",
      name: "home",
      component: HomeView,
    },
    {
      path: "/about",
      component: () => import("../views/AboutView.vue"),
    },
    {
      path: "/login",
      component: () => import("../views/LoginView.vue"),
    },
    {
      path: "/signup",
      component: () => import("../views/SignupView.vue"),
    },
    {
      path: "/dashboard",
      component: () => import("../views/DashboardView.vue"),
      meta: { hideAuthButtons: true },
    },
    {
      path: "/matches",
      component: () => import("../views/MatchesView.vue"),
      meta: { hideAuthButtons: true },
    },
    {
      path: "/message",
      component: () => import("../views/MessageView.vue"),
      meta: { hideAuthButtons: true },
    },
  ],
});

export default router;
