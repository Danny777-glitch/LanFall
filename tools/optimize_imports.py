import os
import re

def optimize_texture_import(import_path):
    if not os.path.exists(import_path):
        return
    with open(import_path, 'r', encoding='utf-8') as f:
        content = f.read()

    fname = os.path.basename(import_path).replace('.import', '').lower()
    
    is_normal = 'nor' in fname or 'normal' in fname
    is_arm = 'arm' in fname or 'rough' in fname or 'ao' in fname or 'orm' in fname
    
    # We want VRAM Compressed (mode=2), mipmaps=true
    content = re.sub(r'compress/mode=\d+', 'compress/mode=2', content)
    content = re.sub(r'mipmaps/generate=\w+', 'mipmaps/generate=true', content)
    
    if is_normal:
        content = re.sub(r'compress/normal_map=\d+', 'compress/normal_map=1', content)
        content = re.sub(r'compress/high_quality=\w+', 'compress/high_quality=false', content)
    elif is_arm:
        content = re.sub(r'compress/normal_map=\d+', 'compress/normal_map=0', content)
        content = re.sub(r'compress/high_quality=\w+', 'compress/high_quality=true', content)
        # ARM/ORM must not be sRGB
        content = re.sub(r'detect_3d/compress_to=\d+', 'detect_3d/compress_to=1', content)
    else: # diffuse / albedo
        content = re.sub(r'compress/normal_map=\d+', 'compress/normal_map=0', content)
        content = re.sub(r'compress/high_quality=\w+', 'compress/high_quality=true', content)
        
    with open(import_path, 'w', encoding='utf-8') as f:
        f.write(content)

def scan_and_optimize(dir_path):
    for root, dirs, files in os.walk(dir_path):
        for f in files:
            if f.endswith('.import') and not f.endswith('.hdr.import'):
                optimize_texture_import(os.path.join(root, f))

if __name__ == '__main__':
    scan_and_optimize('assets/textures/pbr_4k')
    print('Optimized .import files in assets/textures/pbr_4k')
