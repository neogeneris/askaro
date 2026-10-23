#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import json, time, urllib.request, os

data = json.load(open('/tmp/sus.json'))
glosses = data['glosses']
cache_f = '/tmp/zh_cache.json'
cache = json.load(open(cache_f)) if os.path.exists(cache_f) else {}

def google(q):
    url = 'https://translate.googleapis.com/translate_a/single?client=gtx&sl=es&tl=zh-CN&dt=t&q=' + urllib.parse.quote(q)
    req = urllib.request.Request(url, headers={'User-Agent':'Mozilla/5.0'})
    with urllib.request.urlopen(req, timeout=10) as r:
        j = json.loads(r.read().decode())
    return ''.join(seg[0] for seg in j[0] if seg[0])

import urllib.parse
todo = [g for g in glosses if g not in cache]
print(f'todo: {len(todo)}')
B = 46
for i in range(0, len(todo), B):
    chunk = todo[i:i+B]
    # batch via newline join (google supports multi-sentence)
    try:
        res = google('\n'.join(chunk))
        parts = [p for p in res.split('\n')]
        if len(parts) == len(chunk):
            for g,p in zip(chunk,parts): cache[g]=p.strip()
        else:
            raise Exception('split mismatch')
    except Exception as e:
        for g in chunk:
            try: cache[g] = google(g).strip(); time.sleep(0.12)
            except Exception as e2: cache[g] = ''
    json.dump(cache, open(cache_f,'w'), ensure_ascii=False)
    print(i+len(chunk), flush=True)
print('done', len([v for v in cache.values() if v]))
