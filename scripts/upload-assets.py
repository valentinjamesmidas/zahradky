"""Upload build assets using a short-lived Pages JWT, read only from hidden stdin.
Never writes the credential to disk or prints it. prepare-upload.mjs runs first.
"""
import json,getpass,urllib.request
with open('work/upload.json') as f:assets=json.load(f)
token=getpass.getpass('Ready for Pages upload token (input hidden): ')
def api(path,body):
    request=urllib.request.Request('https://api.cloudflare.com/client/v4'+path,data=json.dumps(body).encode(),headers={'Authorization':'Bearer '+token,'Content-Type':'application/json'})
    with urllib.request.urlopen(request,timeout=120) as r:result=json.load(r)
    if not result.get('success'):raise RuntimeError('Asset upload failed: '+str(result.get('errors')))
    return result.get('result')
hashes=[a['key'] for a in assets]
missing=set(api('/pages/assets/check-missing',{'hashes':hashes}))
for start in range(0,len(assets),10):
    batch=[a for a in assets[start:start+10] if a['key'] in missing]
    if batch:api('/pages/assets/upload',batch)
api('/pages/assets/upsert-hashes',{'hashes':hashes})
print('Uploaded and registered',len(assets),'assets successfully.')
