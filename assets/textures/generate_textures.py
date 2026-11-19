"""
LAN Fall - High Quality Stylized Seamless Texture Generator
Generates clean, stylized 512x512 textures optimized for GL Compatibility renderer.
Now with distinct Valorant-style Site A, Site B, and Mid architectural palettes!
"""
import os
import math
import random
from PIL import Image, ImageDraw, ImageFilter, ImageFont

TEXTURE_DIR = os.path.dirname(os.path.abspath(__file__))

def create_cobblestone():
    size = 512
    img = Image.new("RGB", (size, size), (68, 65, 62))
    draw = ImageDraw.Draw(img)
    
    cols, rows = 8, 8
    cw = size / cols
    ch = size / rows
    random.seed(42)
    
    for r in range(rows):
        for c in range(cols):
            x_offset = (random.random() - 0.5) * 8
            y_offset = (random.random() - 0.5) * 8
            x0 = c * cw + 4 + x_offset
            y0 = r * ch + 4 + y_offset
            x1 = (c + 1) * cw - 4 + x_offset
            y1 = (r + 1) * ch - 4 + y_offset
            
            base_shade = random.randint(105, 130)
            tint = random.randint(-6, 6)
            stone_color = (base_shade + tint, base_shade, base_shade - tint - 4)
            highlight = (min(255, stone_color[0] + 20), min(255, stone_color[1] + 20), min(255, stone_color[2] + 16))
            shadow = (max(0, stone_color[0] - 25), max(0, stone_color[1] - 25), max(0, stone_color[2] - 25))
            
            draw.rounded_rectangle([x0, y0, x1, y1], radius=10, fill=stone_color, outline=shadow, width=3)
            draw.arc([x0+3, y0+3, x1-3, y1-3], start=180, end=270, fill=highlight, width=2)
            
    img = img.filter(ImageFilter.SMOOTH_MORE)
    img.save(os.path.join(TEXTURE_DIR, "cobblestone_street.png"))
    print("Created cobblestone_street.png")

# --- Site A: Kingdom Tech / Clean Coastal Architecture (Cool Slate White / Light Cyan) ---
def create_brick_site_a():
    size = 512
    # Cool modern light-slate stucco base
    img = Image.new("RGB", (size, size), (225, 230, 238))
    draw = ImageDraw.Draw(img)
    
    rows = 10
    brick_h = size / rows
    mortar_col = (160, 172, 190)
    
    for r in range(rows):
        y0 = r * brick_h
        y1 = (r + 1) * brick_h
        draw.line([(0, y0), (size, y0)], fill=mortar_col, width=3)
        
        cols = 5
        brick_w = size / cols
        offset = (brick_w / 2) if (r % 2 == 1) else 0
        
        for c in range(-1, cols + 2):
            x = c * brick_w + offset
            draw.line([(x, y0), (x, y1)], fill=mortar_col, width=3)
            
            shade = random.randint(-8, 8)
            b_col = (max(0, min(255, 225 + shade)), max(0, min(255, 230 + shade)), max(0, min(255, 238 + shade + 4)))
            draw.rectangle([x + 3, y0 + 3, x + brick_w - 3, y1 - 3], fill=b_col)
            
    # Add subtle blue-tinted architectural bottom trim stripe
    draw.rectangle([0, size - 24, size, size], fill=(50, 75, 110))
    draw.line([(0, size - 24), (size, size - 24)], fill=(80, 180, 220), width=3)
    
    img = img.filter(ImageFilter.SMOOTH)
    img.save(os.path.join(TEXTURE_DIR, "brick_site_a.png"))
    print("Created brick_site_a.png")

# --- Site B: Industrial Warehouse / Aged Tuscan Sandstone (Warm Golden Ochre / Brick) ---
def create_brick_site_b():
    size = 512
    # Warm golden ochre sandstone
    img = Image.new("RGB", (size, size), (210, 175, 125))
    draw = ImageDraw.Draw(img)
    
    rows = 12
    brick_h = size / rows
    mortar_col = (150, 120, 85)
    
    for r in range(rows):
        y0 = r * brick_h
        y1 = (r + 1) * brick_h
        draw.line([(0, y0), (size, y0)], fill=mortar_col, width=3)
        
        cols = 6
        brick_w = size / cols
        offset = (brick_w / 2) if (r % 2 == 1) else 0
        
        for c in range(-1, cols + 2):
            x = c * brick_w + offset
            draw.line([(x, y0), (x, y1)], fill=mortar_col, width=3)
            
            shade = random.randint(-12, 12)
            b_col = (max(0, min(255, 210 + shade)), max(0, min(255, 175 + shade - 2)), max(0, min(255, 125 + shade - 6)))
            draw.rectangle([x + 3, y0 + 3, x + brick_w - 3, y1 - 3], fill=b_col)
            
    # Add industrial orange caution stripe on bottom edge
    draw.rectangle([0, size - 20, size, size], fill=(180, 80, 25))
    draw.line([(0, size - 20), (size, size - 20)], fill=(240, 130, 40), width=3)
    
    img = img.filter(ImageFilter.SMOOTH)
    img.save(os.path.join(TEXTURE_DIR, "brick_site_b.png"))
    print("Created brick_site_b.png")

# --- Mid Market: Venetian Terracotta Plaster / Stucco (Rich Warm Terracotta / Burnt Sienna) ---
def create_brick_mid():
    size = 512
    img = Image.new("RGB", (size, size), (195, 105, 82))
    draw = ImageDraw.Draw(img)
    
    rows = 10
    brick_h = size / rows
    mortar_col = (145, 75, 58)
    
    for r in range(rows):
        y0 = r * brick_h
        y1 = (r + 1) * brick_h
        draw.line([(0, y0), (size, y0)], fill=mortar_col, width=3)
        
        cols = 6
        brick_w = size / cols
        offset = (brick_w / 2) if (r % 2 == 1) else 0
        
        for c in range(-1, cols + 2):
            x = c * brick_w + offset
            draw.line([(x, y0), (x, y1)], fill=mortar_col, width=3)
            
            shade = random.randint(-10, 10)
            b_col = (max(0, min(255, 195 + shade)), max(0, min(255, 105 + shade - 2)), max(0, min(255, 82 + shade - 4)))
            draw.rectangle([x + 3, y0 + 3, x + brick_w - 3, y1 - 3], fill=b_col)
            
    img = img.filter(ImageFilter.SMOOTH)
    img.save(os.path.join(TEXTURE_DIR, "brick_mid.png"))
    print("Created brick_mid.png")

# --- Site A Slate/Navy High-Tech Roof Tiles ---
def create_roof_slate_navy():
    size = 512
    img = Image.new("RGB", (size, size), (42, 55, 75))
    draw = ImageDraw.Draw(img)
    
    rows = 10
    row_h = size / rows
    for r in range(rows):
        y0 = r * row_h
        y1 = (r + 1) * row_h
        cols = 8
        col_w = size / cols
        for c in range(cols):
            x0 = c * col_w
            x1 = (c + 1) * col_w
            draw.rectangle([x0, y0, x1, y1], fill=(52, 68, 92))
            draw.line([(x0, y0), (x1, y0)], fill=(75, 98, 130), width=2)
            draw.line([(x0, y1), (x1, y1)], fill=(28, 38, 52), width=3)
            draw.line([(x0, y0), (x0, y1)], fill=(32, 42, 58), width=2)
            
    img = img.filter(ImageFilter.SMOOTH)
    img.save(os.path.join(TEXTURE_DIR, "roof_slate_navy.png"))
    print("Created roof_slate_navy.png")

# --- Valorant Style Site Callout Banners ("A" & "B") ---
def create_site_banners():
    size = 512
    # Banner A: Deep Navy banner with vibrant Cyan "A" & Chevron
    img_a = Image.new("RGB", (size, size), (25, 35, 50))
    draw_a = ImageDraw.Draw(img_a)
    draw_a.rectangle([16, 16, size-16, size-16], outline=(40, 180, 220), width=8)
    draw_a.rectangle([28, 28, size-28, size-28], outline=(15, 22, 32), width=4)
    # Big bold "A"
    cx, cy = size // 2, size // 2 - 20
    draw_a.polygon([(cx, cy - 140), (cx + 100, cy + 120), (cx + 55, cy + 120), (cx + 35, cy + 60), (cx - 35, cy + 60), (cx - 55, cy + 120), (cx - 100, cy + 120)], fill=(35, 215, 235))
    draw_a.polygon([(cx, cy - 60), (cx + 20, cy + 20), (cx - 20, cy + 20)], fill=(25, 35, 50))
    # Subtitle "SITE A" bar
    draw_a.rectangle([cx - 140, cy + 150, cx + 140, cy + 195], fill=(35, 215, 235))
    draw_a.polygon([(cx - 50, cy + 215), (cx + 50, cy + 215), (cx, cy + 245)], fill=(35, 215, 235))
    img_a.save(os.path.join(TEXTURE_DIR, "banner_site_a.png"))
    print("Created banner_site_a.png")

    # Banner B: Dark Charcoal banner with vibrant Amber/Orange "B"
    img_b = Image.new("RGB", (size, size), (38, 30, 25))
    draw_b = ImageDraw.Draw(img_b)
    draw_b.rectangle([16, 16, size-16, size-16], outline=(245, 140, 30), width=8)
    draw_b.rectangle([28, 28, size-28, size-28], outline=(20, 16, 14), width=4)
    # Big bold "B"
    draw_b.rounded_rectangle([cx - 80, cy - 140, cx + 70, cy - 15], radius=25, fill=(245, 140, 30))
    draw_b.rounded_rectangle([cx - 45, cy - 110, cx + 35, cy - 45], radius=15, fill=(38, 30, 25))
    draw_b.rounded_rectangle([cx - 80, cy - 10, cx + 80, cy + 120], radius=28, fill=(245, 140, 30))
    draw_b.rounded_rectangle([cx - 45, cy + 18, cx + 45, cy + 92], radius=15, fill=(38, 30, 25))
    draw_b.rectangle([cx - 80, cy - 140, cx - 40, cy + 120], fill=(245, 140, 30))
    # Subtitle "SITE B" bar
    draw_b.rectangle([cx - 140, cy + 150, cx + 140, cy + 195], fill=(245, 140, 30))
    draw_b.polygon([(cx - 50, cy + 215), (cx + 50, cy + 215), (cx, cy + 245)], fill=(245, 140, 30))
    img_b.save(os.path.join(TEXTURE_DIR, "banner_site_b.png"))
    print("Created banner_site_b.png")

def create_terracotta():
    size = 512
    img = Image.new("RGB", (size, size), (165, 68, 40))
    draw = ImageDraw.Draw(img)
    rows = 10
    row_h = size / rows
    for r in range(rows):
        y0 = r * row_h
        y1 = (r + 1) * row_h
        cols = 8
        col_w = size / cols
        for c in range(cols):
            x0 = c * col_w
            x1 = (c + 1) * col_w
            draw.rectangle([x0, y0, x1, y1], fill=(190, 80, 48))
            draw.line([(x0, y0), (x1, y0)], fill=(220, 105, 70), width=2)
            draw.line([(x0, y1), (x1, y1)], fill=(115, 38, 20), width=3)
            draw.line([(x0, y0), (x0, y1)], fill=(125, 42, 22), width=2)
            
    img = img.filter(ImageFilter.SMOOTH)
    img.save(os.path.join(TEXTURE_DIR, "terracotta_tiles.png"))
    print("Created terracotta_tiles.png")

def create_radianite_panel():
    size = 512
    img = Image.new("RGB", (size, size), (22, 28, 36))
    draw = ImageDraw.Draw(img)
    draw.rectangle([10, 10, size-10, size-10], outline=(40, 52, 68), width=6)
    draw.rectangle([20, 20, size-20, size-20], outline=(15, 20, 26), width=4)
    for corner in [(15, 15), (size-15, 15), (15, size-15), (size-15, size-15)]:
        draw.ellipse([corner[0]-8, corner[1]-8, corner[0]+8, corner[1]+8], fill=(20, 190, 180), outline=(220, 255, 250))
    cx, cy = size // 2, size // 2
    draw.polygon([(cx, cy - 100), (cx + 100, cy), (cx, cy + 100), (cx - 100, cy)], fill=(16, 120, 115), outline=(35, 220, 210))
    draw.polygon([(cx, cy - 65), (cx + 65, cy), (cx, cy + 65), (cx - 65, cy)], fill=(25, 185, 175), outline=(180, 255, 250))
    draw.polygon([(cx, cy - 35), (cx + 35, cy), (cx, cy + 35), (cx - 35, cy)], fill=(190, 255, 250))
    draw.line([(cx - 100, cy), (30, cy)], fill=(30, 200, 190), width=3)
    draw.line([(cx + 100, cy), (size - 30, cy)], fill=(30, 200, 190), width=3)
    draw.line([(cx, cy - 100), (cx, 30)], fill=(30, 200, 190), width=3)
    draw.line([(cx, cy + 100), (cx, size - 30)], fill=(30, 200, 190), width=3)
    img = img.filter(ImageFilter.SMOOTH)
    img.save(os.path.join(TEXTURE_DIR, "radianite_panel.png"))
    print("Created radianite_panel.png")

def create_wood_planks():
    size = 512
    img = Image.new("RGB", (size, size), (135, 92, 58))
    draw = ImageDraw.Draw(img)
    plank_count = 6
    plank_h = size / plank_count
    for i in range(plank_count):
        y0 = i * plank_h
        y1 = (i + 1) * plank_h
        var = random.randint(-15, 15)
        base = (145 + var, 98 + var, 62 + var)
        draw.rectangle([0, y0, size, y1], fill=base)
        draw.line([(0, y0), (size, y0)], fill=(85, 52, 30), width=4)
        draw.line([(0, y0+3), (size, y0+3)], fill=(175, 125, 80), width=2)
    img = img.filter(ImageFilter.SMOOTH)
    img.save(os.path.join(TEXTURE_DIR, "wood_planks.png"))
    print("Created wood_planks.png")

def create_metal_trim():
    size = 512
    img = Image.new("RGB", (size, size), (45, 50, 56))
    draw = ImageDraw.Draw(img)
    draw.rectangle([10, 10, size-10, size-10], outline=(65, 72, 80), width=4)
    draw.line([(0, size//2), (size, size//2)], fill=(28, 30, 34), width=6)
    draw.line([(0, size//2 - 2), (size, size//2 - 2)], fill=(80, 88, 98), width=2)
    for x in range(30, size, 60):
        for y in [24, size//2 - 18, size//2 + 18, size - 24]:
            draw.ellipse([x-4, y-4, x+4, y+4], fill=(75, 82, 92), outline=(22, 25, 28))
    img = img.filter(ImageFilter.SMOOTH)
    img.save(os.path.join(TEXTURE_DIR, "metal_trim.png"))
    print("Created metal_trim.png")

def create_tactical_crate():
    size = 512
    img = Image.new("RGB", (size, size), (215, 110, 22))
    draw = ImageDraw.Draw(img)
    bracket_col = (40, 42, 46)
    b_size = 64
    for corner in [(0, 0), (size - b_size, 0), (0, size - b_size), (size - b_size, size - b_size)]:
        draw.rectangle([corner[0], corner[1], corner[0] + b_size, corner[1] + b_size], fill=bracket_col)
    draw.line([(40, 40), (size-40, size-40)], fill=(180, 85, 12), width=22)
    draw.line([(size-40, 40), (40, size-40)], fill=(180, 85, 12), width=22)
    draw.line([(40, 40), (size-40, size-40)], fill=(235, 135, 40), width=8)
    draw.line([(size-40, 40), (40, size-40)], fill=(235, 135, 40), width=8)
    draw.rectangle([15, 15, size-15, size-15], outline=(145, 65, 8), width=10)
    draw.rectangle([size//2 - 60, size//2 - 30, size//2 + 60, size//2 + 30], fill=(32, 35, 38))
    draw.line([(size//2 - 50, size//2), (size//2 + 50, size//2)], fill=(250, 195, 35), width=6)
    img = img.filter(ImageFilter.SMOOTH)
    img.save(os.path.join(TEXTURE_DIR, "crate_tactical.png"))
    print("Created crate_tactical.png")

if __name__ == "__main__":
    create_cobblestone()
    create_brick_site_a()
    create_brick_site_b()
    create_brick_mid()
    create_roof_slate_navy()
    create_site_banners()
    create_terracotta()
    create_radianite_panel()
    create_wood_planks()
    create_metal_trim()
    create_tactical_crate()
    print("ALL VALORANT-THEMED TEXTURES GENERATED SUCCESSFULLY!")
