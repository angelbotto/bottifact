#!/usr/bin/env python3
"""Valida la entrada portable, enlaces locales y presencia de recursos de esta biblioteca."""
from pathlib import Path
import re,json
ROOT=Path(__file__).resolve().parents[1]
s=(ROOT/'SKILL.md').read_text();assert s.startswith('---\n');front,body=s[4:].split('\n---\n',1)
fields=dict(re.findall(r'^([\w-]+):\s*(.+)$',front,re.M));name=fields.get('name','');desc=fields.get('description','')
assert re.fullmatch(r'[a-z0-9]+(?:-[a-z0-9]+)*',name) and len(name)<=64
assert 1<=len(desc)<=1024 and len(fields.get('compatibility',''))<=500
assert len(s.splitlines())<500 and len(body.split())<5000
assert '/Users/' not in s and 'app://' not in s
for link in re.findall(r'\]\(([^)]+)\)',s):
 if not link.startswith(('http:','https:','#')):assert (ROOT/link.split('#')[0]).is_file(),link
assert (ROOT/'agents/openai.yaml').is_file()
version=json.loads((ROOT/'VERSION.json').read_text());registry=json.loads((ROOT/'packages/core/registry/registry.json').read_text())
assert version['componentes']==len(registry['componentes'])
assert version['skill']==name=='bottifact' and version['nombre']=='Bottifact'
ui=(ROOT/'agents/openai.yaml').read_text()
assert 'display_name: "Bottifact"' in ui and '$'+name in ui
print(f'Skill portable: {len(s.splitlines())} líneas, enlaces vigentes y {len(registry["componentes"])} recetas. Compatible con el formato Agent Skills; no acredita carga automática de un agente.')
