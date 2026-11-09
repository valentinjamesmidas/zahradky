import {onRequest} from '../functions/api/leads.js';
export default {async fetch(request,env){const url=new URL(request.url);if(url.pathname==='/api/leads')return onRequest({request,env});if(url.pathname.startsWith('/api/'))return Response.json({error:'Tato služba neexistuje.'},{status:404});return env.ASSETS.fetch(request)}};
