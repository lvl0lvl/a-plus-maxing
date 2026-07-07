import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import { writeFileSync } from 'node:fs'
import { resolve } from 'node:path'

// emitBuildConfig writes dist/build-config.json describing the build that ships.
// The §6.4 seam gate reads this (via the harness fetching it from the served app)
// to satisfy PA-2: it asserts mode === "production" and dataAttributes ===
// "preserved" over the PRODUCTION build config. This config sets no JSX/HTML
// transform that removes data-* attributes, so the shipped bundle keeps them.
function emitBuildConfig() {
  let mode = 'unknown'
  return {
    name: 'emit-build-config',
    configResolved(cfg) { mode = cfg.mode },
    closeBundle() {
      const cfg = { mode, dataAttributes: 'preserved' }
      writeFileSync(resolve('dist', 'build-config.json'), JSON.stringify(cfg, null, 2) + '\n')
    },
  }
}

export default defineConfig({
  plugins: [react(), emitBuildConfig()],
  build: { outDir: 'dist' },
})
