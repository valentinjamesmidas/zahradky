import test from 'node:test';
import assert from 'node:assert/strict';
import {readFile,stat} from 'node:fs/promises';
import {defaultConfig,calculate,validateConfig,serializableConfig,normalizeConfig,houses,gardenOptions,techOptions} from '../src/catalog.js';
import {expandedOptions,setOption} from '../src/expandedCatalog.js';

test('Old shared configurations retain their choices and gain disabled new options',()=>{
 const old=Object.fromEntries(Object.entries(defaultConfig).filter(([k])=>!k.startsWith('extra_')));
 assert.ok(validateConfig(old));
 const next=normalizeConfig(old);assert.deepEqual(serializableConfig(next),defaultConfig);
 assert.equal(calculate(old).total,calculate(next).total);
});
test('Unpriced concepts survive serialization and do not masquerade as free equipment',()=>{
 const next=setOption({...defaultConfig,house:'studio'},'extra_sauna',true);
 assert.ok(validateConfig(next));assert.equal(serializableConfig(next).extra_sauna,true);
 const quote=calculate(next);assert.equal(quote.unpriced.length,2);
 assert.deepEqual(quote.unpriced.map(i=>i.price),[null,null]);
 assert.equal(quote.total,calculate({...defaultConfig,house:'none'}).total);
 assert.ok(Number.isFinite(quote.monthly));
});
test('Equipment slots replace collisions and enforce terrace dependencies on client and server',()=>{
 let c=setOption(defaultConfig,'extra_sauna',true);
 c=setOption(c,'extra_tub',true);assert.equal(c.extra_sauna,false);assert.equal(c.extra_tub,true);
 c=setOption(c,'extra_greenhouse',true);c=setOption(c,'beds',true);assert.equal(c.extra_greenhouse,false);
 c=setOption({...c,terrace:false},'extra_dining',true);assert.equal(c.terrace,true);
 c=setOption(c,'terrace',false);assert.equal(c.extra_dining,false);assert.ok(validateConfig(c));
 assert.equal(validateConfig({...defaultConfig,extra_sauna:true,extra_pool:true}),false);
 assert.equal(validateConfig({...defaultConfig,terrace:false,extra_dining:true}),false);
 assert.equal(validateConfig({...defaultConfig,extra_sauna:'yes'}),false);
});
test('All 20 added models are self-contained GLBs with a bounded material/mesh budget',async()=>{
 const options=[...houses.filter(h=>h.concept),...expandedOptions];assert.equal(options.length,20);
 for(const o of options){
  const b=await readFile(`public/models/${o.model}.glb`);assert.equal(b.toString('ascii',0,4),'glTF');assert.equal(b.readUInt32LE(8),b.length);
  const j=JSON.parse(b.toString('utf8',20,20+b.readUInt32LE(12)));
  assert.ok(j.meshes.length<=14,o.id);assert.ok(j.buffers.every(b=>!b.uri),o.id);
  assert.ok(!j.images?.some(i=>i.uri),o.id);assert.ok(b.length<500000,o.id);
 }
});
test('Every visual option has a usable small local thumbnail',async()=>{
 for(const o of [...houses.filter(h=>h.id!=='none'),...gardenOptions,...techOptions]){
  const s=await stat(`public${o.preview}`);assert.ok(s.size>500,o.id);assert.ok(s.size<200000,o.id);
 }
});
test('Optimized default scene reduces static mesh submissions by at least 90 percent',async()=>{
 const report=JSON.parse(await readFile('docs/model-optimization.json','utf8'));
 const names=['plot_base','orchard_trees','tiny_liberte','terrace'];
 const before=names.reduce((n,k)=>n+report[k].before.primitives,0),after=names.reduce((n,k)=>n+report[k].after.primitives,0);
 assert.ok(after<before*.1,`${before} -> ${after}`);
});
