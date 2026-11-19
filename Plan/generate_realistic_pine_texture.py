import numpy as np
from PIL import Image, ImageDraw
import math
import random

def generate_pine_bough():
    random.seed(42)
    np.random.seed(42)
    
    width = 1024
    height = 1024
    img = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    # 1. Main tapered central wooden stem/twig
    # from bottom center (512, 980) to top center (512, 100)
    stem_points = []
    num_stem = 100
    for i in range(num_stem):
        t = i / float(num_stem)
        y = 980 - t * 860
        # gentle natural bend
        x = 512 + math.sin(t * 4.0) * 12.0
        w = (1.0 - t * 0.75) * 14.0
        stem_points.append((x, y, w))
        
    for i in range(len(stem_points) - 1):
        x1, y1, w1 = stem_points[i]
        x2, y2, w2 = stem_points[i+1]
        col = (68, 48, 32, 255)
        draw.line([(x1, y1), (x2, y2)], fill=col, width=int(w1))

    # 2. Side sub-twigs
    sub_twigs = []
    for i in range(15, 85, 3):
        x_stem, y_stem, _ = stem_points[i]
        t = i / 100.0
        twig_len = (1.0 - t * 0.6) * 220.0 * random.uniform(0.85, 1.15)
        
        # Left twig
        angle_l = math.radians(random.uniform(125, 145))
        ex_l = x_stem + math.cos(angle_l) * twig_len
        ey_l = y_stem - math.sin(angle_l) * twig_len * 0.6
        draw.line([(x_stem, y_stem), (ex_l, ey_l)], fill=(58, 42, 28, 240), width=int(max(2, 6 * (1.0 - t))))
        sub_twigs.append((x_stem, y_stem, ex_l, ey_l, t))
        
        # Right twig
        angle_r = math.radians(random.uniform(35, 55))
        ex_r = x_stem + math.cos(angle_r) * twig_len
        ey_r = y_stem - math.sin(angle_r) * twig_len * 0.6
        draw.line([(x_stem, y_stem), (ex_r, ey_r)], fill=(58, 42, 28, 240), width=int(max(2, 6 * (1.0 - t))))
        sub_twigs.append((x_stem, y_stem, ex_r, ey_r, t))

    # 3. Dense pine needles along main stem and all sub-twigs
    needle_layer = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    needle_draw = ImageDraw.Draw(needle_layer)

    def draw_needle_cluster(origin_x, origin_y, base_angle, length, count):
        for _ in range(count):
            ang = base_angle + math.radians(random.uniform(-25, 25))
            nl = length * random.uniform(0.7, 1.2)
            nx = origin_x + math.cos(ang) * nl
            ny = origin_y - math.sin(ang) * nl
            
            # Natural needle color variation (forest green, moss green, olive, dark spruce)
            shade = random.uniform(0.8, 1.25)
            r = int(min(255, max(0, 32 * shade)))
            g = int(min(255, max(0, 68 * shade + random.uniform(-6, 6))))
            b = int(min(255, max(0, 36 * shade)))
            a = int(random.uniform(220, 255))
            
            needle_draw.line([(origin_x, origin_y), (nx, ny)], fill=(r, g, b, a), width=random.choice([2, 3, 3, 4]))

    # Needles along main stem
    for i in range(10, 95):
        x_stem, y_stem, _ = stem_points[i]
        t = i / 100.0
        n_len = (1.0 - t * 0.5) * 85.0
        # left needles
        draw_needle_cluster(x_stem, y_stem, math.radians(random.uniform(130, 160)), n_len, 6)
        # right needles
        draw_needle_cluster(x_stem, y_stem, math.radians(random.uniform(20, 50)), n_len, 6)
        # upward needles
        draw_needle_cluster(x_stem, y_stem, math.radians(random.uniform(75, 105)), n_len * 0.8, 4)

    # Needles along sub-twigs
    for (sx, sy, ex, ey, t) in sub_twigs:
        steps = 15
        for s in range(steps):
            frac = s / float(steps)
            px = sx + (ex - sx) * frac
            py = sy + (ey - sy) * frac
            n_len = (1.0 - t * 0.4) * 65.0 * (1.0 - frac * 0.3)
            
            dx = ex - sx
            dy = ey - sy
            base_ang = math.atan2(-dy, dx)
            
            draw_needle_cluster(px, py, base_ang + math.radians(35), n_len, 4)
            draw_needle_cluster(px, py, base_ang - math.radians(35), n_len, 4)
            draw_needle_cluster(px, py, base_ang, n_len * 0.9, 3)

    # Composite layers
    img = Image.alpha_composite(img, needle_layer)
    
    # Save realistic pine branch texture
    out_path = r"c:\Users\danie\Documents\my_projects\lan-fall-phase1\assets\textures\pine_branch_realistic.png"
    img.save(out_path, "PNG")
    print("Saved high-res realistic pine branch texture:", out_path)

generate_pine_bough()
