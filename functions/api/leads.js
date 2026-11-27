import {calculate,validateConfig,serializableConfig} from '../../src/catalog.js';
import {sites, contact} from '../../src/offer.js';
const headers={'Content-Type':'application/json; charset=utf-8','Cache-Control':'no-store','X-Content-Type-Options':'nosniff'};
const json=(body,status=200)=>new Response(JSON.stringify(body),{status,headers});
async function readBody(request){
 const size=Number(request.headers.get('Content-Length'));
 if(size>10000)throw new Error('size');
 const reader=request.body?.getReader();if(!reader)throw new Error('json');let total=0;const chunks=[];
 while(true){const {done,value}=await reader.read();if(done)break;total+=value.byteLength;if(total>10000){await reader.cancel();throw new Error('size')}chunks.push(value)}
 const bytes=new Uint8Array(total);let offset=0;for(const chunk of chunks){bytes.set(chunk,offset);offset+=chunk.byteLength}
 return JSON.parse(new TextDecoder().decode(bytes));
}
export async function onRequestPost({request,env}){
 const url=new URL(request.url),origin=request.headers.get('Origin');
 if((origin&&origin!==url.origin)||request.headers.get('Sec-Fetch-Site')==='cross-site')return json({error:'Odeslání z této stránky není povoleno.'},403);
 if(!request.headers.get('Content-Type')?.startsWith('application/json'))return json({error:'Neplatný formát požadavku.'},415);
 let body;try{body=await readBody(request)}catch(e){return json({error:e.message==='size'?'Poptávka je příliš dlouhá.':'Poptávku se nepodařilo přečíst.'},e.message==='size'?413:400)}
 if(!body||typeof body!=='object')return json({error:'Neplatná poptávka.'},400);
 if(body.website)return json({error:'Poptávku nebylo možné ověřit.'},400);
 const text=(v,max)=>typeof v==='string'&&v.trim().length<=max?v.trim():'';
 const name=text(body.name,120),email=text(body.email,200),phone=text(body.phone,30),note=text(body.note??'',2000),requestId=text(body.requestId,36);
 const visit=body.intent==='visit';
 if(body.intent!==undefined&&!['visit','quote'].includes(body.intent))return json({error:'Neplatný druh požadavku.'},400);
 const validContact=/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)&&body.consent===true;
 const validId=/^[0-9a-f]{8}-[0-9a-f]{4}-4[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$/i.test(requestId);
 const validQuote=name.length>=2&&/^\+?[0-9 ()-]{9,30}$/.test(phone)&&phone.replace(/\D/g,'').length>=9&&phone.replace(/\D/g,'').length<=15&&typeof (body.note??'')==='string'&&(body.note??'').length<=2000&&typeof body.reserve==='boolean'&&validateConfig(body.config);
 if(!validContact||!validId||(visit?!sites.some(site=>site.id===body.location):!validQuote))return json({error:'Zkontrolujte kontaktní údaje, souhlas a zvolenou lokalitu.'},400);
 if(!env.DB)return json({error:'Příjem poptávek je dočasně nedostupný. Uložte si konfiguraci a zkuste to později.'},503);
 try{
  const existing=await env.DB.prepare('SELECT code FROM project_requests WHERE request_id = ?').bind(requestId).first();
  if(existing)return json({ok:true,code:existing.code},200);
  const now=Math.floor(Date.now()/1000),window=Math.floor(now/3600);
  const digest=await crypto.subtle.digest('SHA-256',new TextEncoder().encode(`${request.headers.get('CF-Connecting-IP')||'unknown'}:${window}`));
  const key=Array.from(new Uint8Array(digest)).map(x=>x.toString(16).padStart(2,'0')).join('');
  const rate=await env.DB.prepare('INSERT INTO rate_limits (key, window, count) VALUES (?, ?, 1) ON CONFLICT(key, window) DO UPDATE SET count = count + 1 RETURNING count').bind(key,window).first();
  if(rate.count>6)return json({error:'Přijali jsme příliš mnoho poptávek. Zkuste to prosím později.'},429);
  const nowLocation=visit?body.location:body.config.location;
  const prefix=visit?'PR-'+nowLocation:'CZ-'+nowLocation+'-'+String(body.config.plot).padStart(2,'0');
  const code=prefix+'-'+requestId.slice(0,8).toUpperCase();
  const batch=[
   env.DB.prepare('DELETE FROM leads WHERE created_at < ?').bind(now-90*86400),
   env.DB.prepare('DELETE FROM project_requests WHERE created_at < ?').bind(now-90*86400),
   env.DB.prepare('DELETE FROM rate_limits WHERE window < ?').bind(window-24),
   env.DB.prepare('INSERT INTO project_requests (request_id,code,intent,location,visit_email,assigned_to,created_at) VALUES (?,?,?,?,?,?,?) ON CONFLICT(request_id) DO NOTHING').bind(requestId,code,visit?'visit':'quote',nowLocation,visit?email:null,contact.email,now)
  ];
  if(!visit){
   const config=serializableConfig(body.config),summary=calculate(config);
   batch.push(env.DB.prepare(`INSERT INTO leads (request_id, code, name, email, phone, note, reservation_requested, configuration, total, down_payment, monthly, created_at)
    SELECT ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ? WHERE EXISTS (SELECT 1 FROM project_requests WHERE request_id=? AND intent='quote') ON CONFLICT(request_id) DO NOTHING`)
    .bind(requestId,code,name,email,phone,note,body.reserve?1:0,JSON.stringify(config),summary.total,summary.down,summary.monthly,now,requestId));
  }
  batch.push(env.DB.prepare('SELECT code FROM project_requests WHERE request_id=?').bind(requestId));
  const batchResults=await env.DB.batch(batch);
  const savedCode=batchResults.at(-1).results[0].code;
  return json({ok:true,code:savedCode},batchResults[3].meta.changes?201:200);
 }catch{
  console.error(JSON.stringify({event:'lead_storage_failed'}));
  return json({error:'Poptávku se nepodařilo uložit. Váš návrh zůstává zachovaný; zkuste to prosím znovu.'},503);
 }
}
export function onRequest({request,env}){if(request.method==='POST')return onRequestPost({request,env});return new Response(JSON.stringify({error:'Použijte odeslání formuláře.'}),{status:405,headers:{...headers,Allow:'POST'}})}
