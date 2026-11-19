import os
import math
import random
from PIL import Image, ImageDraw, ImageFilter

TEXTURE_DIR = "c:/Users/danie/Documents/my_projects/lan-fall-phase1/assets/textures"
os.makedirs(TEXTURE_DIR, exist_ok=True)


def make_normal_map(albedo_img, strength=2.5):
    """Converts a grayscale or RGB image to a realistic tangent-space normal map."""
    gray = albedo_img.convert("L")
    w, h = gray.size
    pixels = gray.load()
    norm = Image.new("RGB", (w, h))
    norm_pix = norm.load()

    for y in range(h):
        for x in range(w):
            left = pixels[(x - 1) % w, y]
            right = pixels[(x + 1) % w, y]
            up = pixels[x, (y - 1) % h]
            down = pixels[x, (y + 1) % h]

            dx = (right - left) / 255.0 * strength
            dy = (down - up) / 255.0 * strength
            dz = 1.0

            length = math.sqrt(dx * dx + dy * dy + dz * dz)
            nx = dx / length
            ny = dy / length
            nz = dz / length

            r = int((nx * 0.5 + 0.5) * 255)
            g = int((-ny * 0.5 + 0.5) * 255) # Green channel inverted for DirectX/Godot
            b = int((nz * 0.5 + 0.5) * 255)
            norm_pix[x, y] = (r, g, b)

    return norm


# 1. Train Freight Car Siding (Corrugated metal with rivet bands)
def create_train_boxcar():
    img = Image.new("RGB", (512, 512), (75, 55, 45)) # Warm oxidized industrial steel
    draw = ImageDraw.Draw(img)
    # Vertical corrugations
    for x in range(512):
        wave = math.sin(x * 0.25) * 24
        for y in range(512):
            noise = random.randint(-8, 8)
            v = int(wave + noise)
            r = min(255, max(0, 82 + v))
            g = min(255, max(0, 58 + int(v * 0.85)))
            b = min(255, max(0, 48 + int(v * 0.7)))
            draw.point((x, y), fill=(r, g, b))
    # Horizontal structural steel bands with rivets
    for y_pos in [40, 256, 470]:
        draw.rectangle([0, y_pos - 12, 512, y_pos + 12], fill=(45, 38, 34))
        # Rivets
        for rx in range(16, 512, 32):
            draw.ellipse([rx - 4, y_pos - 4, rx + 4, y_pos + 4], fill=(130, 115, 100))
            draw.ellipse([rx - 2, y_pos - 2, rx + 2, y_pos + 2], fill=(190, 175, 160))

    img.save(os.path.join(TEXTURE_DIR, "train_boxcar_albedo.png"))
    norm = make_normal_map(img, strength=3.0)
    norm.save(os.path.join(TEXTURE_DIR, "train_boxcar_normal.png"))
    print("Generated train_boxcar textures.")


# 2. Wooden Fence with Top Diamond Lattice
def create_wood_lattice_fence():
    img = Image.new("RGB", (512, 512), (105, 82, 58)) # Weathered rustic cedar
    draw = ImageDraw.Draw(img)
    # Bottom 70%: Vertical wooden fence pickets
    picket_w = 42
    for px in range(0, 512, picket_w):
        # Board shading
        tone = random.randint(-15, 15)
        for x in range(px + 2, px + picket_w - 2):
            for y in range(160, 512):
                wood_grain = int(math.sin(y * 0.08 + x * 0.02) * 12 + random.randint(-6, 6))
                r = min(255, max(0, 115 + tone + wood_grain))
                g = min(255, max(0, 88 + int(tone * 0.85) + wood_grain))
                b = min(255, max(0, 62 + int(tone * 0.7) + wood_grain))
                draw.point((x, y), fill=(r, g, b))
        # Picket gap shadow
        draw.rectangle([px, 160, px + 2, 512], fill=(30, 22, 16))
    # Horizontal fence rails
    draw.rectangle([0, 150, 512, 165], fill=(70, 50, 32))
    draw.rectangle([0, 470, 512, 485], fill=(70, 50, 32))

    # Top 30%: Diamond cross-hatch lattice
    draw.rectangle([0, 0, 512, 150], fill=(50, 38, 28)) # Dark backing
    # Diagonal slats /
    for d in range(-512, 1024, 28):
        draw.line([(d, 0), (d + 200, 150)], fill=(125, 98, 70), width=6)
    # Diagonal slats \
    for d in range(-512, 1024, 28):
        draw.line([(d, 0), (d - 200, 150)], fill=(110, 85, 60), width=6)

    # Top capping rail
    draw.rectangle([0, 0, 512, 18], fill=(65, 48, 32))

    img.save(os.path.join(TEXTURE_DIR, "wood_fence_lattice_albedo.png"))
    norm = make_normal_map(img, strength=2.8)
    norm.save(os.path.join(TEXTURE_DIR, "wood_fence_lattice_normal.png"))
    print("Generated wood_fence_lattice textures.")


# 3. Terracotta Roof Tiles (for Villa and Barn roofs)
def create_terracotta_tiles():
    img = Image.new("RGB", (512, 512), (180, 85, 52)) # Rich Mediterranean terracotta
    draw = ImageDraw.Draw(img)
    tile_w = 42
    tile_h = 64
    for row in range(0, 512, tile_h):
        offset = (row // tile_h % 2) * (tile_w // 2)
        for col in range(-tile_w, 512 + tile_w, tile_w):
            x1 = col + offset
            x2 = x1 + tile_w
            y1 = row
            y2 = row + tile_h
            # Curved barrel tile shading
            var = random.randint(-12, 12)
            for x in range(x1, x2):
                if 0 <= x < 512:
                    curve = math.sin((x - x1) / tile_w * math.pi)
                    shading = int(curve * 45) + var
                    for y in range(y1, y2):
                        if 0 <= y < 512:
                            r = min(255, max(0, 165 + shading))
                            g = min(255, max(0, 75 + int(shading * 0.6)))
                            b = min(255, max(0, 48 + int(shading * 0.4)))
                            draw.point((x, y), fill=(r, g, b))
            # Tile bottom overlap shadow
            rx0 = max(0, x1)
            rx1 = min(511, x2)
            if rx0 <= rx1:
                draw.rectangle([rx0, y2 - 4, rx1, y2], fill=(60, 25, 15))

    img.save(os.path.join(TEXTURE_DIR, "roof_terracotta_rich_albedo.png"))
    norm = make_normal_map(img, strength=3.2)
    norm.save(os.path.join(TEXTURE_DIR, "roof_terracotta_rich_normal.png"))
    print("Generated terracotta tile textures.")


# 4. White Villa Stucco Facade with Timber Framing
def create_villa_facade():
    img = Image.new("RGB", (512, 512), (232, 226, 215)) # Warm ivory plaster
    draw = ImageDraw.Draw(img)
    # Subtle stucco texture
    for y in range(512):
        for x in range(512):
            n = random.randint(-8, 8)
            draw.point((x, y), fill=(232 + n, 226 + n, 215 + n))

    # Timber beam corner quoining / framing
    draw.rectangle([0, 0, 36, 512], fill=(95, 68, 48))
    draw.rectangle([476, 0, 512, 512], fill=(95, 68, 48))
    draw.rectangle([0, 0, 512, 24], fill=(85, 60, 42))
    draw.rectangle([0, 248, 512, 272], fill=(85, 60, 42)) # Mid-floor dividing beam

    # European Window with green shutters
    wx, wy, ww, wh = 160, 70, 192, 140
    # Window Frame
    draw.rectangle([wx - 6, wy - 6, wx + ww + 6, wy + wh + 6], fill=(55, 40, 28))
    # Shutters (left and right)
    draw.rectangle([wx - 48, wy - 4, wx - 6, wy + wh + 4], fill=(68, 92, 75)) # Sage green
    draw.rectangle([wx + ww + 6, wy - 4, wx + ww + 48, wy + wh + 4], fill=(68, 92, 75))
    # Shutter louvers
    for ly in range(wy + 8, wy + wh, 12):
        draw.line([(wx - 44, ly), (wx - 10, ly)], fill=(45, 62, 50), width=2)
        draw.line([(wx + ww + 10, ly), (wx + ww + 44, ly)], fill=(45, 62, 50), width=2)
    # Glass Panes (paned warm reflection)
    draw.rectangle([wx, wy, wx + ww, wy + wh], fill=(40, 52, 65))
    draw.line([(wx + ww//2, wy), (wx + ww//2, wy + wh)], fill=(220, 215, 205), width=4)
    draw.line([(wx, wy + wh//2), (wx + ww, wy + wh//2)], fill=(220, 215, 205), width=4)

    img.save(os.path.join(TEXTURE_DIR, "villa_facade_albedo.png"))
    norm = make_normal_map(img, strength=2.2)
    norm.save(os.path.join(TEXTURE_DIR, "villa_facade_normal.png"))
    print("Generated villa_facade textures.")


# 5. Concrete Jersey / Highway Barrier
def create_jersey_barrier():
    img = Image.new("RGB", (512, 512), (175, 172, 168)) # Industrial cured concrete
    draw = ImageDraw.Draw(img)
    for y in range(512):
        for x in range(512):
            grain = random.randint(-14, 14)
            # Dirt and grime at base
            grime = int((y / 512.0) ** 2 * 45)
            r = min(255, max(0, 175 + grain - grime))
            g = min(255, max(0, 172 + grain - grime))
            b = min(255, max(0, 168 + grain - int(grime * 1.2)))
            draw.point((x, y), fill=(r, g, b))

    # Top beveled edge highlight
    draw.rectangle([0, 0, 512, 12], fill=(210, 208, 204))
    # Drain slots / forklift holes at bottom
    for fx in [100, 340]:
        draw.rectangle([fx, 430, fx + 72, 485], fill=(45, 42, 40))

    img.save(os.path.join(TEXTURE_DIR, "jersey_barrier_albedo.png"))
    norm = make_normal_map(img, strength=2.5)
    norm.save(os.path.join(TEXTURE_DIR, "jersey_barrier_normal.png"))
    print("Generated jersey_barrier textures.")


# 6. Blue Slate Roofing for Spawn Twin Sheds
def create_spawn_shed_roof():
    img = Image.new("RGB", (512, 512), (48, 65, 85)) # Deep tactical slate blue
    draw = ImageDraw.Draw(img)
    # Corrugated lines
    for x in range(512):
        wave = int(math.sin(x * 0.35) * 32)
        for y in range(512):
            n = random.randint(-8, 8)
            v = wave + n
            r = min(255, max(0, 52 + v))
            g = min(255, max(0, 72 + int(v * 1.1)))
            b = min(255, max(0, 95 + int(v * 1.2)))
            draw.point((x, y), fill=(r, g, b))

    img.save(os.path.join(TEXTURE_DIR, "spawn_shed_roof_albedo.png"))
    norm = make_normal_map(img, strength=2.8)
    norm.save(os.path.join(TEXTURE_DIR, "spawn_shed_roof_normal.png"))
    print("Generated spawn_shed_roof textures.")


create_train_boxcar()
create_wood_lattice_fence()
create_terracotta_tiles()
create_villa_facade()
create_jersey_barrier()
create_spawn_shed_roof()
print("ALL BGMI TDM TEXTURES GENERATED SUCCESSFULLY!")
