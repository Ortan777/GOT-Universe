from PIL import Image, ImageDraw, ImageFont
import os

# Colors for different houses
house_colors = {
    'targaryen': '#4A0404',
    'stark': '#2C3E50',
    'lannister': '#C5A028',
    'baratheon': '#8B0000',
    'greyjoy': '#2F4F4F',
    'tyrell': '#228B22',
    'martell': '#FF6B35',
    'tully': '#1E4D6E',
    'arryn': '#87CEEB',
    'default': '#4A4A4A'
}

# Create placeholder images for each house
for house, color in house_colors.items():
    # Create a 200x200 image
    img = Image.new('RGB', (200, 200), color)
    draw = ImageDraw.Draw(img)
    
    # Add text
    try:
        font = ImageFont.truetype("arial.ttf", 24)
    except:
        font = ImageFont.load_default()
    
    text = house.upper()
    bbox = draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    
    position = ((200 - text_width) // 2, (200 - text_height) // 2)
    draw.text(position, text, fill='white', font=font)
    
    # Draw a dragon/crown indicator for special characters
    draw.ellipse([50, 50, 150, 150], outline='gold', width=3)
    
    # Save
    img.save(f"../{house}/placeholder.jpg")

print("Placeholder images created!")