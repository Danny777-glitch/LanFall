with open('scenes/maps/warehouse/props/bgmi_spawn_sheds.tscn', 'r', encoding='utf-8') as f:
    text = f.read()

import re
matches = re.finditer(r'\[sub_resource type="StandardMaterial3D" id="([^"]+)"\](.*?)(?=\n\[)', text, re.DOTALL)
for m in matches:
    print(f"=== {m.group(1)} ===")
    print(m.group(2).strip())
