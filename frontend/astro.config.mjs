import { defineConfig } from 'astro/config';
import vue from '@astrojs/vue';
import tailwind from '@astrojs/tailwind';
import sitemap from '@astrojs/sitemap';

// https://astro.build/config
export default defineConfig({
  site: 'https://your-event-booking-site.com', // Update with your domain
  integrations: [
    vue({
      // Vue configuration
      appEntrypoint: '/src/app.ts',
      devtools: true
    }),
    tailwind({
      // Tailwind configuration - let Astro handle the PostCSS setup
      applyBaseStyles: true
    }),
    sitemap({
      // Generate sitemap for SEO
      changefreq: 'weekly',
      priority: 0.7,
      lastmod: new Date(),
    })
  ],
  
  // Build configuration
  build: {
    // Inline stylesheets smaller than this size
    inlineStylesheets: 'auto',
  },
  
  // Development server configuration
  server: {
    port: 4321,
    host: true // Allow external connections
  },
  
  // Output configuration
  output: 'static', // Can be changed to 'server' for SSR
  
  // Image optimization
  image: {
    domains: ['images.unsplash.com', 'via.placeholder.com'],
    remotePatterns: [
      {
        protocol: 'https'
      }
    ]
  },
  
  // Vite configuration
  vite: {
    // CSS configuration
    css: {
      devSourcemap: true
    },
    
    // Build optimization
    build: {
      // Chunk splitting for better caching
      rollupOptions: {
        output: {
          manualChunks: {
            'vue-vendor': ['vue'],
            'utils': ['@vueuse/core', 'zod'],
            'icons': ['lucide-vue-next']
          }
        }
      }
    },
    
    // Development configuration
    define: {
      __DEV__: JSON.stringify(process.env.NODE_ENV === 'development')
    }
  },
  
  // Markdown configuration
  markdown: {
    // Syntax highlighting
    shikiConfig: {
      theme: 'github-dark',
      wrap: true
    }
  },
  
  // View transitions are now stable in Astro 4.x
  // No experimental flag needed
});