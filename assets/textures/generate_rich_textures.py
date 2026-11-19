import os
import math
import random
from PIL import Image, ImageDraw, ImageFilter, ImageFont

TEXTURE_DIR = os.path.dirname(os.path.abspath(__file__))

def create_market_awning():
    size = 512
    img = Image.new("RGB", (size, size), (220, 220, 220))
    draw = ImageDraw.Draw(img)
    stripe_w = size // 8
    # Alternating vibrant Venetian Red and Cream stripes
    for i in range(8):
        col = (185, 45, 45) if i % 2 == 0 else (240, 235, 225)
        draw.rectangle([i * stripe_w, 0, (i + 1) * stripe_w, size], fill=col)
        # Subtle fabric fold shadow
        draw.line([(i * stripe_w, 0), (i * stripe_w, size)], fill=(40, 40, 40, 60), width=2)
    img = img.filter(ImageFilter.SMOOTH)
    img.save(os.path.join(TEXTURE_DIR, "market_awning_stripe.png"), "PNG")
    print("Created market_awning_stripe.png")

def create_warning_stripes():
    size = 512
    img = Image.new("RGB", (size, size), (245, 195, 30))
    draw = ImageDraw.Draw(img)
    stripe_w = 48
    # Diagonal hazard stripes
    for x in range(-size, size * 2, stripe_w * 2):
        points = [
            (x, 0),
            (x + stripe_w, 0),
            (x + stripe_w - size, size),
            (x - size, size)
        ]
        draw.polygon(points, fill=(28, 30, 34))
    img.save(os.path.join(TEXTURE_DIR, "warning_stripes.png"), "PNG")
    print("Created warning_stripes.png")

def create_site_stencils():
    size = 512
    # Site A: Cyan tactical marker
    img_a = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    draw_a = ImageDraw.Draw(img_a)
    draw_a.rounded_rectangle([32, 32, size-32, size-32], radius=32, outline=(30, 210, 255, 240), width=16)
    # Stencil Letter "A"
    draw_a.polygon([(size//2, 90), (size//2 - 130, 420), (size//2 - 60, 420), (size//2 - 30, 320), (size//2 + 30, 320), (size//2 + 60, 420), (size//2 + 130, 420)], fill=(30, 210, 255, 240))
    draw_a.polygon([(size//2, 170), (size//2 - 25, 260), (size//2 + 25, 260)], fill=(0, 0, 0, 0))
    img_a.save(os.path.join(TEXTURE_DIR, "site_stencil_a.png"), "PNG")
    print("Created site_stencil_a.png")

    # Site B: Ochre/Amber tactical marker
    img_b = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    draw_b = ImageDraw.Draw(img_b)
    draw_b.rounded_rectangle([32, 32, size-32, size-32], radius=32, outline=(255, 175, 40, 240), width=16)
    # Stencil Letter "B"
    draw_b.rounded_rectangle([130, 100, 360, 250], radius=40, fill=(255, 175, 40, 240))
    draw_b.rounded_rectangle([130, 250, 380, 420], radius=40, fill=(255, 175, 40, 240))
    draw_b.rounded_rectangle([210, 140, 300, 210], radius=15, fill=(0, 0, 0, 0))
    draw_b.rounded_rectangle([210, 290, 310, 370], radius=15, fill=(0, 0, 0, 0))
    img_b.save(os.path.join(TEXTURE_DIR, "site_stencil_b.png"), "PNG")
    print("Created site_stencil_b.png")

if __name__ == "__main__":
    create_market_awning()
    create_warning_stripes()
    create_site_stencils()
