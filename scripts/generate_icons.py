"""Generate PWA icon PNGs for FPL League Analysis.

Creates a purple rounded-square icon with a white soccer ball emoji.
Run once: python scripts/generate_icons.py
"""

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

STATIC_DIR = Path(__file__).resolve().parent.parent / "static"
BG_COLOR = (55, 0, 60)  # #37003c
SIZES = {
    "icon-512.png": 512,
    "icon-192.png": 192,
    "apple-touch-icon.png": 180,
}


def _draw_soccer_ball(draw: ImageDraw.ImageDraw, cx: int, cy: int, r: int) -> None:
    """Draw a simplified soccer ball (circle + pentagon pattern) in white."""
    # Outer circle
    draw.ellipse(
        [cx - r, cy - r, cx + r, cy + r],
        fill="white",
    )

    # Draw pentagon-style pattern lines (simplified geometric soccer ball)
    import math

    inner_r = int(r * 0.38)
    outer_r = int(r * 0.78)
    line_w = max(2, r // 25)

    # Draw 5 dark pentagons/patches for soccer ball look
    for i in range(5):
        angle = math.radians(90 + i * 72)
        px = cx + int(inner_r * math.cos(angle))
        py = cy - int(inner_r * math.sin(angle))

        # Small pentagon at each vertex
        patch_r = int(r * 0.22)
        points = []
        for j in range(5):
            a = angle + math.radians(j * 72)
            points.append((
                px + int(patch_r * 0.45 * math.cos(a)),
                py - int(patch_r * 0.45 * math.sin(a)),
            ))
        draw.polygon(points, fill=BG_COLOR)

        # Line from center to outer edge
        ox = cx + int(outer_r * math.cos(angle))
        oy = cy - int(outer_r * math.sin(angle))
        draw.line([(px, py), (ox, oy)], fill=BG_COLOR, width=line_w)

    # Center pentagon
    center_r = int(r * 0.22)
    center_points = []
    for i in range(5):
        angle = math.radians(90 + i * 72)
        center_points.append((
            cx + int(center_r * math.cos(angle)),
            cy - int(center_r * math.sin(angle)),
        ))
    draw.polygon(center_points, fill=BG_COLOR)


def generate_icon(size: int) -> Image.Image:
    """Generate a single icon at the given size."""
    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    # Rounded rectangle background
    margin = int(size * 0.05)
    radius = int(size * 0.18)
    draw.rounded_rectangle(
        [margin, margin, size - margin, size - margin],
        radius=radius,
        fill=BG_COLOR,
    )

    # Soccer ball in center
    cx, cy = size // 2, size // 2
    ball_r = int(size * 0.28)
    _draw_soccer_ball(draw, cx, cy, ball_r)

    return img


def main() -> None:
    STATIC_DIR.mkdir(exist_ok=True)
    for filename, size in SIZES.items():
        img = generate_icon(size)
        path = STATIC_DIR / filename
        img.save(path, "PNG")
        print(f"Generated {path} ({size}x{size})")


if __name__ == "__main__":
    main()
