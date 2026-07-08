import subprocess
import time
import urllib.request
import json
import urllib.error
import sys

# Start uvicorn
proc = subprocess.Popen(['uvicorn', 'main:app', '--port', '8005'], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
time.sleep(5) # Wait for it to start

try:
    req = urllib.request.Request('http://127.0.0.1:8005/ai/extract', data=json.dumps({'message':'remove the follow-up'}).encode('utf-8'), headers={'Content-Type':'application/json'})
    res = urllib.request.urlopen(req)
    print("Response:", res.read().decode('utf-8'))
except urllib.error.URLError as e:
    print('URLError:', e)
finally:
    # Check if process is still alive
    poll = proc.poll()
    if poll is None:
        print("Uvicorn is still running!")
        proc.terminate()
    else:
        print("Uvicorn CRASHED with exit code:", poll)
        out, _ = proc.communicate()
        print("UVICORN OUTPUT:", out.decode('utf-8', errors='ignore'))
