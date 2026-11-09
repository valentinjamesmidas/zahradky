import {build} from 'esbuild';
await build({entryPoints:['scripts/worker-entry.js'],outfile:'dist/_worker.js',bundle:true,format:'esm',platform:'browser',target:'es2022',minify:true});
console.log('Pages API worker built.');
