/**
 * 应用入口文件
 * 创建 Vue 实例，注册 Pinia 和路由，引入全局样式
 */
import { createApp } from 'vue'
import { createPinia } from 'pinia'
import App from './App.vue'
import router from './router'
import './assets/styles/main.scss'

const app = createApp(App)
app.use(createPinia())
app.use(router)
app.mount('#app')
