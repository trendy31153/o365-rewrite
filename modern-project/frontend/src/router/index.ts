import { createRouter, createWebHistory, RouteRecordRaw } from "vue-router";
import { useSessionStore } from "../stores/session";
import DashboardView from "../views/DashboardView.vue";
import InvitesView from "../views/InvitesView.vue";
import LicensesView from "../views/LicensesView.vue";
import LoginView from "../views/LoginView.vue";
import ReportsView from "../views/ReportsView.vue";
import SettingsView from "../views/SettingsView.vue";
import TenantsView from "../views/TenantsView.vue";
import UsersView from "../views/UsersView.vue";

const routes: Array<RouteRecordRaw> = [
  { path: "/login", name: "login", component: LoginView },
  {
    path: "/",
    component: DashboardView,
    children: [
      { path: "", redirect: "/tenants" },
      { path: "tenants", name: "tenants", component: TenantsView },
      { path: "users", name: "users", component: UsersView },
      { path: "licenses", name: "licenses", component: LicensesView },
      { path: "invites", name: "invites", component: InvitesView },
      { path: "reports", name: "reports", component: ReportsView },
      { path: "settings", name: "settings", component: SettingsView }
    ]
  }
];

const router = createRouter({
  history: createWebHistory(),
  routes
});

router.beforeEach(async (to, _from, next) => {
  const session = useSessionStore();
  if (session.token && !session.username) {
    try {
      await session.loadProfile();
    } catch (error) {
      console.error("Failed to hydrate session", error);
      session.signOut();
    }
  }

  if (to.name !== "login" && !session.isAuthenticated) {
    next({ name: "login" });
  } else {
    next();
  }
});

export default router;
