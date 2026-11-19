import os
import math
import random
from PIL import Image, ImageDraw, ImageFilter

TEXTURE_DIR = os.path.dirname(os.path.abspath(__file__))
WIDTH = 2048
HEIGHT = 1024

def create_valorant_sky():
    # 1. Base Sky Gradient (Ascent Mediterranean Azure)
    img = Image.new("RGB", (WIDTH, HEIGHT))
    draw = ImageDraw.Draw(img)
    
    # Zenith deep blue -> Upper azure -> Horizon warm glow -> Ground haze
    for y in range(HEIGHT):
        ratio = y / float(HEIGHT)
        if ratio < 0.48: # Sky Zenith to upper
            t = ratio / 0.48
            # (30, 105, 225) -> (95, 175, 245)
            r = int(30 * (1 - t) + 95 * t)
            g = int(105 * (1 - t) + 175 * t)
            b = int(225 * (1 - t) + 245 * t)
        elif ratio < 0.58: # Horizon warm golden haze
            t = (ratio - 0.48) / 0.10
            # (95, 175, 245) -> (220, 235, 252)
            r = int(95 * (1 - t) + 220 * t)
            g = int(175 * (1 - t) + 235 * t)
            b = int(245 * (1 - t) + 252 * t)
        elif ratio < 0.70: # Horizon to ground warm bounce
            t = (ratio - 0.58) / 0.12
            # (220, 235, 252) -> (170, 185, 205)
            r = int(220 * (1 - t) + 170 * t)
            g = int(235 * (1 - t) + 185 * t)
            b = int(252 * (1 - t) + 205 * t)
        else: # Ground lower bounce
            t = (ratio - 0.70) / 0.30
            # (170, 185, 205) -> (80, 95, 115)
            r = int(170 * (1 - t) + 80 * t)
            g = int(185 * (1 - t) + 95 * t)
            b = int(205 * (1 - t) + 115 * t)
        draw.line([(0, y), (WIDTH, y)], fill=(r, g, b))

    # 2. Add Warm Radiant Sun Disc and Corona (around X=600, Y=380)
    sun_x = 640
    sun_y = 380
    
    # Broad atmospheric solar corona
    corona = Image.new("RGBA", (WIDTH, HEIGHT), (0, 0, 0, 0))
    c_draw = ImageDraw.Draw(corona)
    for radius in range(350, 20, -10):
        alpha = int((1.0 - (radius / 350.0)) ** 2 * 110)
        c_draw.ellipse([sun_x - radius, sun_y - radius * 0.7, sun_x + radius, sun_y + radius * 0.7], fill=(255, 245, 210, alpha))
    
    # Core bright sun disc
    c_draw.ellipse([sun_x - 36, sun_y - 28, sun_x + 36, sun_y + 28], fill=(255, 255, 245, 240))
    c_draw.ellipse([sun_x - 18, sun_y - 14, sun_x + 18, sun_y + 14], fill=(255, 255, 255, 255))
    
    img = Image.alpha_composite(img.convert("RGBA"), corona).convert("RGB")

    # 3. Stylized Cumulus Clouds (Valorant painted puff style)
    cloud_layer = Image.new("RGBA", (WIDTH, HEIGHT), (0, 0, 0, 0))
    cdraw = ImageDraw.Draw(cloud_layer)

    random.seed(42) # Consistent gorgeous clouds

    def draw_stylized_cloud(cx, cy, scale_w, scale_h):
        # Multi-puff cumulus shape
        puffs = [
            (0, 0, 1.0, 0.75),
            (-0.35, 0.1, 0.75, 0.6),
            (0.35, 0.08, 0.8, 0.65),
            (-0.65, 0.22, 0.55, 0.45),
            (0.65, 0.2, 0.6, 0.5),
            (-0.15, -0.22, 0.7, 0.55),
            (0.2, -0.25, 0.65, 0.5),
        ]
        # Base shadow underside
        for px, py, pw, ph in puffs:
            rx = int(pw * scale_w * 0.5)
            ry = int(ph * scale_h * 0.5)
            x0 = int(cx + px * scale_w - rx)
            y0 = int(cy + py * scale_h - ry + scale_h * 0.15)
            x1 = int(cx + px * scale_w + rx)
            y1 = int(cy + py * scale_h + ry + scale_h * 0.15)
            cdraw.ellipse([x0, y0, x1, y1], fill=(165, 185, 215, 160))
        # Mid tone body
        for px, py, pw, ph in puffs:
            rx = int(pw * scale_w * 0.48)
            ry = int(ph * scale_h * 0.48)
            x0 = int(cx + px * scale_w - rx)
            y0 = int(cy + py * scale_h - ry + scale_h * 0.05)
            x1 = int(cx + px * scale_w + rx)
            y1 = int(cy + py * scale_h + ry + scale_h * 0.05)
            cdraw.ellipse([x0, y0, x1, y1], fill=(225, 235, 250, 210))
        # Sunlit bright highlight
        for px, py, pw, ph in puffs:
            rx = int(pw * scale_w * 0.42)
            ry = int(ph * scale_h * 0.42)
            x0 = int(cx + px * scale_w - rx)
            y0 = int(cy + py * scale_h - ry - scale_h * 0.08)
            x1 = int(cx + px * scale_w + rx)
            y1 = int(cy + py * scale_h + ry - scale_h * 0.08)
            cdraw.ellipse([x0, y0, x1, y1], fill=(255, 255, 255, 235))

    # Cluster of heroic clouds across the sky
    cloud_positions = [
        (320, 360, 260, 110),
        (520, 330, 320, 130),
        (850, 380, 240, 100),
        (1150, 340, 380, 150),
        (1480, 370, 310, 120),
        (1820, 350, 340, 140),
        (120, 390, 280, 110),
        # Distant low wisps
        (250, 470, 200, 60),
        (720, 460, 250, 70),
        (1350, 480, 220, 65),
        (1700, 465, 240, 70),
    ]

    for cx, cy, sw, sh in cloud_positions:
        draw_stylized_cloud(cx, cy, sw, sh)

    # Soften clouds to look like painterly atmospheric sky
    cloud_layer = cloud_layer.filter(ImageFilter.GaussianBlur(radius=3.5))
    final_sky = Image.alpha_composite(img.convert("RGBA"), cloud_layer).convert("RGB")

    output_path = os.path.join(TEXTURE_DIR, "sky_valorant_ascent.png")
    final_sky.save(output_path, "PNG", quality=95)
    print("SUCCESS: Generated Valorant sky at:", output_path)

if __name__ == "__main__":
    create_valorant_sky()
