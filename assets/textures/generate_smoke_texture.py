import os
import math
import random
from PIL import Image, ImageDraw, ImageFilter

TEXTURE_DIR = os.path.dirname(os.path.abspath(__file__))

def create_smoke_puff():
    size = 256
    # Create RGBA image
    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    center = size / 2.0
    radius = size * 0.42
    
    # Generate multi-lobed organic cloud puff
    random.seed(1337)
    lobes = [
        (0, 0, radius * 0.75, 230),
        (-25, -20, radius * 0.6, 200),
        (30, -15, radius * 0.58, 210),
        (-20, 25, radius * 0.55, 190),
        (25, 20, radius * 0.62, 205),
        (-35, 5, radius * 0.45, 170),
        (35, -5, radius * 0.48, 180),
        (5, -35, radius * 0.42, 160),
        (-5, 35, radius * 0.45, 175)
    ]
    
    draw = ImageDraw.Draw(img)
    for lx, ly, lr, alpha in lobes:
        cx = center + lx
        cy = center + ly
        # Radial gradient circle
        for r in range(int(lr), 0, -2):
            t = r / float(lr)
            # Soft smoothstep falloff
            a = int(alpha * (1.0 - t * t))
            # Stylized smoke color: cool charcoal/slate with subtle teal tint
            col = (200, 215, 230, a)
            draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=col)
            
    # Apply soft blur for smooth volumetric look
    img = img.filter(ImageFilter.GaussianBlur(radius=8))
    out_path = os.path.join(TEXTURE_DIR, "smoke_puff.png")
    img.save(out_path, "PNG")
    print("Created smoke_puff.png successfully!")

if __name__ == "__main__":
    create_smoke_puff()
