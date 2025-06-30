import os
from pathlib import Path
from PIL import Image

# Config
image_folder = Path("./images")  # Path to folder containing full-size images
thumb_folder = image_folder / "thumbs"
output_file = "index.html"
thumb_size = (300, 300)  # Max width, height for thumbnails

# Ensure thumbnail directory exists
thumb_folder.mkdir(exist_ok=True)

# Supported image formats
image_extensions = ('.jpg', '.jpeg', '.png', '.gif', '.webp', '.bmp')

# Generate thumbnails
for img_file in sorted(image_folder.iterdir()):
    if img_file.suffix.lower() in image_extensions:
        thumb_file = thumb_folder / img_file.name
        if not thumb_file.exists():
            try:
                with Image.open(img_file) as img:
                    img.thumbnail(thumb_size)
                    img.save(thumb_file)
                    print(f"✔️ Created thumbnail: {thumb_file}")
            except Exception as e:
                print(f"❌ Failed to process {img_file}: {e}")

# Generate HTML
html_head = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Image Gallery</title>
    <style>
        body {{ font-family: sans-serif; margin: 20px; }}
        .gallery {{ display: flex; flex-wrap: wrap; gap: 10px; }}
        .gallery a {{ text-decoration: none; }}
        .gallery img {{
            max-width: {thumb_size[0]}px;
            height: auto;
            border: 1px solid #ccc;
            border-radius: 4px;
        }}
    </style>
</head>
<body>
<h1>Image Gallery</h1>
<div class="gallery">
"""

html_tail = """
</div>
</body>
</html>
"""

# Insert image tags
gallery_html = ""
for img_file in sorted(image_folder.iterdir()):
    if img_file.suffix.lower() in image_extensions:
        thumb_path = thumb_folder / img_file.name
        gallery_html += f'  <a href="{img_file}" target="_blank"><img src="{thumb_path}" alt="{img_file.name}"></a>\n'

# Write final HTML file
with open(output_file, 'w', encoding='utf-8') as f:
    f.write(html_head + gallery_html + html_tail)

print(f"\n✅ Gallery created: {output_file}")
