// Uses the operator's existing Cloudflare login. Contact details stay in the private D1 console.
import {spawnSync} from 'node:child_process';
const [action,value] = process.argv.slice(2);
let sql;
if(action==='inbox' && (!value || ['KLD','MBL','PRI'].includes(value))) {
 const filter=value ? " AND intent='visit' AND location='"+value+"'" : '';
 sql="SELECT code,intent,location,email,name,phone,assigned_to,datetime(created_at,'unixepoch') AS received_utc FROM sales_inbox WHERE first_response_at IS NULL"+filter+" ORDER BY created_at";
} else if(action==='replied' && /^(PR-[A-Z]{3}|CZ-[A-Z]{3}-\d{2})-[0-9A-F]{8}$/.test(value||'')) {
 sql="UPDATE project_requests SET first_response_at=coalesce(first_response_at,unixepoch()) WHERE code='"+value+"' RETURNING code,(first_response_at-created_at) AS response_seconds";
} else {
 console.error('Použití: npm run obchod -- inbox [KLD|MBL|PRI] nebo npm run obchod -- replied KÓD');
 process.exit(1);
}
const result=spawnSync('wrangler',['d1','execute','zahradky-leads','--remote','--command',sql],{stdio:'inherit'});
process.exit(result.status ?? 1);
