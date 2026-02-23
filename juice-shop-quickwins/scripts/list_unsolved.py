#!/usr/bin/env python3
"""List unsolved challenges from a Juice Shop /api/Challenges JSON export."""
import json,sys

path = sys.argv[1] if len(sys.argv)>1 else '/tmp/ch.json'
with open(path,'r',encoding='utf-8') as f:
    data=json.load(f)
ch = data.get('data', data)
uns=[c for c in ch if not c.get('solved')]
print(f"unsolved {len(uns)}")
for c in uns:
    print(f"{c.get('key','?')} - {c.get('name','?')}")
