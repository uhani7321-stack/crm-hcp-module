import urllib.request, json, urllib.error
req = urllib.request.Request('http://127.0.0.1:8001/ai/extract', data=json.dumps({'message':'remove the follow-up'}).encode('utf-8'), headers={'Content-Type':'application/json'})
try:
    res = urllib.request.urlopen(req)
    print(res.read().decode('utf-8'))
except urllib.error.URLError as e:
    if hasattr(e, 'read'):
        print('URLError Body:', e.read().decode('utf-8'))
    else:
        print('URLError:', e)
