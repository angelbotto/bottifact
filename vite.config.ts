import { defineConfig } from 'vite';
export default defineConfig({
  root: 'examples/react',
  publicDir: '../../packages/core/assets/table-fixtures',
  server: { host: '127.0.0.1', fs: { allow: ['../..'] } },
  build: { outDir: '../../dist/react-demo', emptyOutDir: true },
  resolve: { dedupe: ['react', 'react-dom'] },
});
