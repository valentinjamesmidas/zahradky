import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';
import tailwindcss from '@tailwindcss/vite';
export default defineConfig({plugins:[react(),tailwindcss()],build:{rollupOptions:{output:{onlyExplicitManualChunks:true,manualChunks(id){
 if(!id.includes('node_modules'))return;
 if(/node_modules\/(react|react-dom|scheduler|react-reconciler)\//.test(id))return 'react';
 if(/node_modules\/three\//.test(id))return 'three-core';
 if(/node_modules\/(@react-three|three-stdlib)\//.test(id))return 'scene-runtime';
}}}}});
