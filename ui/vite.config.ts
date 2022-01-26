import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import path from 'path'

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [vue()],
  resolve:{
    alias:[
      { find: '@', replacement: path.resolve(__dirname, './src') },
      { find: '@views', replacement: path.resolve(__dirname, './src/views') },
      { find: '@components', replacement: path.resolve(__dirname, './src/components') },
    ]
  }
})
