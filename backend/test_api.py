import urllib.request, json, urllib.error
try:
    req1 = urllib.request.Request('http://127.0.0.1:8000/ai/extract', data=json.dumps({'message':'I just had a 45-minute Meeting with Dr. Sarah Jenkins today at 2:00 PM. We discussed the Phase 3 trial results for OncoBoost. She seemed a bit neutral about it. I gave her the clinical trial summary brochure.'}).encode('utf-8'), headers={'Content-Type':'application/json'})
    res1 = urllib.request.urlopen(req1)
    print("Response 1:", res1.read().decode('utf-8'))
except urllib.error.URLError as e:
    if hasattr(e, 'read'):
        print('URLError Body:', e.read().decode('utf-8'))
    else:
        print('URLError:', e)
