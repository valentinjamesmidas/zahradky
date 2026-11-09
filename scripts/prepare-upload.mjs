// Prepare the same content-addressed manifest as Wrangler Pages Direct Upload.
import {readdir,readFile,writeFile} from 'node:fs/promises';
import {extname,join} from 'node:path';
import {hash} from 'blake3-wasm';
const manifest={},assets=[];
const types={'.html':'text/html; charset=utf-8','.js':'application/javascript','.css':'text/css','.json':'application/json','.svg':'image/svg+xml','.glb':'model/gltf-binary','.webp':'image/webp','.blend':'application/octet-stream','.ttf':'font/ttf','.woff2':'font/woff2','.txt':'text/plain; charset=utf-8'};
async function walk(dir,rel=''){for(const f of await readdir(dir,{withFileTypes:true})){const path=join(dir,f.name),name=rel+'/'+f.name;if(f.isDirectory()){await walk(path,name);continue}if(['/_worker.js','/_headers','/_routes.json','/_redirects'].includes(name))continue;const bytes=await readFile(path),value=bytes.toString('base64'),key=hash(value+extname(path).substring(1)).toString('hex').slice(0,32);manifest[name]=key;assets.push({key,value,metadata:{contentType:types[extname(path)]||'application/octet-stream'},base64:true})}}
await walk('dist');await writeFile('work/manifest.json',JSON.stringify(manifest));await writeFile('work/upload.json',JSON.stringify(assets));console.log(`Prepared ${assets.length} static assets.`);
