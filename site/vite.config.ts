import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// GitHub Pages serves the site from /QueryPat/; Vercel serves it from the
// domain root. VERCEL is set automatically in Vercel's build environment.
export default defineConfig({
  plugins: [react()],
  base: process.env.VERCEL ? '/' : '/QueryPat/',
})
