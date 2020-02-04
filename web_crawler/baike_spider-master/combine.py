import json, os

files = os.listdir('./data')[:-1]
with open('baike.json', 'wb', encoding='utf-8') as fp:
    for file in files:
        if file.endswith('.json'):
            with open(os.path.join('data', file), 'rb', encoding='utf-8') as f:
                fp.write(f.read())