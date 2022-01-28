import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import legacy from "@vitejs/plugin-legacy";
import path from 'path'

// https://vitejs.dev/config/
export default defineConfig({
  build:{
    target:"es2015"
  },
  plugins: [
      vue(),
      legacy({
        "targets":["chrome >= 63"]
      })
  ],
  resolve:{
    alias:[
      { find: '@', replacement: path.resolve(__dirname, './src') },
      { find: '@views', replacement: path.resolve(__dirname, './src/views') },
      { find: '@components', replacement: path.resolve(__dirname, './src/components') },
    ]
  }
})
