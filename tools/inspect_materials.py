import os
import re

props_dir = 'scenes/maps/warehouse/props'
all_textures = {}
all_materials = {}

for fname in sorted(os.listdir(props_dir)):
    if not fname.endswith('.tscn'):
        continue
    fpath = os.path.join(props_dir, fname)
    with open(fpath, 'r', encoding='utf-8') as f:
        text = f.read()
    
    ext_tex = re.findall(r'\[ext_resource type="Texture2D"[^\]]+path="([^"]+)" id="([^"]+)"\]', text)
    sub_mats = re.findall(r'\[sub_resource type="StandardMaterial3D" id="([^"]+)"\]', text)
    
    print(f'=== {fname} ===')
    print(f'  Materials ({len(sub_mats)}): {sub_mats}')
    print(f'  Textures ({len(ext_tex)}):')
    for p, i in ext_tex:
        print(f'    [{i}] {p}')
        all_textures[p] = all_textures.get(p, 0) + 1

print('\n=== Texture Usage Summary ===')
for tex, count in sorted(all_textures.items(), key=lambda x: x[1], reverse=True):
    print(f'{count}x : {tex}')
