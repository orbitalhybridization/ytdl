from cairosvg import svg2png
from PIL import Image

# Convert SVG to PNG
svg2png(url="your_icon.svg", write_to="temp_icon.png")

# Convert PNG to ICO
img = Image.open("temp_icon.png")
img.save("your_icon.ico", format="ICO")
