import { defineConfig } from 'astro/config';
import react from '@astrojs/react';

export default defineConfig({
  integrations: [react()],
  site: 'https://kevinhuang001.github.io',
  base: '/peninsula-marketplace/',
  outDir: './docs',
  build: { format: 'file' }
});
