import react from '@vitejs/plugin-react'
import { defineConfig } from 'vite'

// https://vite.dev/config/
export default defineConfig({
  plugins: [react()],
  server: {
    // Forward API calls to the FastAPI dev server so the frontend can use relative /api URLs.
    proxy: {
      '/api': 'http://localhost:8000',
    },
  },
})
