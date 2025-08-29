import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
  plugins: [react()],
  base: './',  // <-- changer ici
  server: {
    port: 5173,
    proxy: {
      '/api': {
        target: 'http://localhost:8000', // backend Django
        changeOrigin: true,
        rewrite: (path) => path.replace(/^\/api/, '/api'),
      },
      '/ws': {
        target: 'ws://localhost:8001', // WebSocket pour notifications
        ws: true,
      },
    },
  },
})
