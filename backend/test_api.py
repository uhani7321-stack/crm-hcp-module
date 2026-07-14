import urllib.request, json, urllib.error
try:
    req1 = urllib.request.Request('http://127.0.0.1:8000/ai/extract', data=json.dumps({'message':'Met Dr. Smith, discussed Prodo-X efficacy, positive sentiment, shared brochure'}).encode('utf-8'), headers={'Content-Type':'application/json'})
    res1 = urllib.request.urlopen(req1)
    print("Response 1:", res1.read().decode('utf-8'))
    
    req2 = urllib.request.Request('http://127.0.0.1:8000/ai/extract', data=json.dumps({'message':'sorry its mr john'}).encode('utf-8'), headers={'Content-Type':'application/json'})
    res2 = urllib.request.urlopen(req2)
    print("Response 2:", res2.read().decode('utf-8'))
except urllib.error.URLError as e:
    if hasattr(e, 'read'):
        print('URLError Body:', e.read().decode('utf-8'))
    else:
        print('URLError:', e)
