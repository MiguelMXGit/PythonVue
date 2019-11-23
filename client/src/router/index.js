import Vue from 'vue';
import VueRouter from 'vue-router';
import LoginComponent from "../views/login.vue"
import GraficaComponent from "../views/grafica.vue"

Vue.use(VueRouter);

export default new VueRouter({
  mode: 'history',
  base: process.env.BASE_URL,
  routes: [
    {
        path: '/',
        redirect: {
            name: "login"
        }
    },
    {
        path: "/login",
        name: "login",
        component: LoginComponent
    },
    {
        path: "/grafica",
        name: "grafica",
        component: GraficaComponent
    }
  ],
});