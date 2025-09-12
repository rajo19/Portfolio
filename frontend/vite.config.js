import { fileURLToPath, URL } from 'node:url'
import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import vuetify from 'vite-plugin-vuetify'

export default defineConfig({
  plugins: [
    vue({
      template: {
        compilerOptions: {
          isCustomElement: (tag) => ['md-linedivider'].includes(tag)
        }
      }
    }),
    vuetify({
      autoImport: true,
      styles: { configFile: 'src/styles/settings.scss' }
    })
  ],
  resolve: {
    alias: {
      '@': fileURLToPath(new URL('./src', import.meta.url))
    }
  },
  server: {
    port: 3000,
    proxy: {
      '/api': {
        target: 'http://localhost:8000',
        changeOrigin: true,
        secure: false,
        ws: true
      }
    }
  },
  css: {
    preprocessorOptions: {
      scss: {
        additionalData: (content, filename) => {
          // Only inject variables into other SCSS files, not into variables.scss itself
          if (filename.includes('variables.scss')) {
            return content;
          }
          return `@import "@/styles/variables.scss";\n${content}`;
        },
        quietDeps: true,
        charset: false,
        logger: {
          warn: function(message, options) {
            // Filter out Vuetify deprecation warnings
            if (message.includes('global-builtin') || 
                message.includes('map-get') || 
                message.includes('vuetify') ||
                message.includes('node_modules/vuetify')) {
              return;
            }
            console.warn(message);
          }
        }
      },
    },
  },
})
