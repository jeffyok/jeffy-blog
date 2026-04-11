/**
 * Vite 构建配置
 * 配置 Vue 插件、路径别名、开发服务器端口和 API 代理
 */
import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import { fileURLToPath, URL } from 'node:url'

export default defineConfig({
  plugins: [vue()],
  resolve: {
    alias: {
      '@': fileURLToPath(new URL('./src', import.meta.url)),  // @ 指向 src 目录
    },
  },
  server: {
    port: 5173,
    // 开发环境将 /api 请求代理到后端服务
    proxy: {
      '/api': {
        target: 'http://localhost:8000',
        changeOrigin: true,
      },
    },
  },
})
