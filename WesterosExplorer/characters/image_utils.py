import os
import requests
from django.core.files.base import ContentFile
from django.conf import settings
from PIL import Image
import io
import hashlib
from pathlib import Path

# Working image sources from reliable APIs and databases
CHARACTER_IMAGE_SOURCES = {
    # Targaryens
    'Daenerys Targaryen': 'https://images.unsplash.com/photo-1546182990-dffeafbe841d?w=400',  # Fantasy queen aesthetic
    'Jon Snow': 'https://images.unsplash.com/photo-1500648767791-00dcc994a43e?w=400',  # Dark hair, brooding
    'Tyrion Lannister': 'https://images.unsplash.com/photo-1472099645785-5658abf4ff4e?w=400',  # Clever look
    'Arya Stark': 'https://images.unsplash.com/photo-1544717301-9cdcb1f5940f?w=400',  # Young warrior
    'Sansa Stark': 'https://images.unsplash.com/photo-1534751516642-a1af1ef26a56?w=400',  # Noble lady
    'Bran Stark': 'https://images.unsplash.com/photo-1533227268428-f9ed0900fb3b?w=400',  # Mysterious
    'Cersei Lannister': 'https://images.unsplash.com/photo-1529626455594-4ff0802cfb7e?w=400',  # Golden hair, queenly
    'Jaime Lannister': 'https://images.unsplash.com/photo-1506794778202-cad84cf45f1d?w=400',  # Handsome knight
    'Aegon I Targaryen': 'https://images.unsplash.com/photo-1608889476561-6242cfdbf622?w=400',  # Conqueror look
    'Rhaenyra Targaryen': 'https://images.unsplash.com/photo-1579033461380-adb47c3eb938?w=400',  # Silver hair
    'Daemon Targaryen': 'https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=400',  # Rogue prince look
    
    # Starks
    'Eddard Stark': 'https://images.unsplash.com/photo-1500648767791-00dcc994a43e?w=400',
    'Catelyn Stark': 'https://images.unsplash.com/photo-1544005313-94ddf0286df2?w=400',
    'Robb Stark': 'https://images.unsplash.com/photo-1506794778202-cad84cf45f1d?w=400',
    'Rickon Stark': 'https://images.unsplash.com/photo-1590086782792-42dd2350140d?w=400',
    
    # Lannisters
    'Tywin Lannister': 'https://images.unsplash.com/photo-1472099645785-5658abf4ff4e?w=400',
    'Kevan Lannister': 'https://images.unsplash.com/photo-1500648767791-00dcc994a43e?w=400',
    
    # Baratheons
    'Robert Baratheon': 'https://images.unsplash.com/photo-1531427186626-4fd8a578f2b5?w=400',
    'Stannis Baratheon': 'https://images.unsplash.com/photo-1519085360753-af0119f7cbe7?w=400',
    'Renly Baratheon': 'https://images.unsplash.com/photo-1506794778202-cad84cf45f1d?w=400',
    
    # Greyjoys
    'Theon Greyjoy': 'https://images.unsplash.com/photo-1492562080023-ab3db95bfbce?w=400',
    'Yara Greyjoy': 'https://images.unsplash.com/photo-1534751516642-a1af1ef26a56?w=400',
    'Euron Greyjoy': 'https://images.unsplash.com/photo-1519085360753-af0119f7cbe7?w=400',
    
    # Tyrells
    'Margaery Tyrell': 'https://images.unsplash.com/photo-1529626455594-4ff0802cfb7e?w=400',
    'Olenna Tyrell': 'https://images.unsplash.com/photo-1544005313-94ddf0286df2?w=400',
    'Loras Tyrell': 'https://images.unsplash.com/photo-1506794778202-cad84cf45f1d?w=400',
    
    # Martells
    'Oberyn Martell': 'https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=400',
    'Ellaria Sand': 'https://images.unsplash.com/photo-1534751516642-a1af1ef26a56?w=400',
    
    # Other major characters
    'Brienne of Tarth': 'https://images.unsplash.com/photo-1544717301-9cdcb1f5940f?w=400',
    'Tormund Giantsbane': 'https://images.unsplash.com/photo-1531427186626-4fd8a578f2b5?w=400',
    'Melisandre': 'https://images.unsplash.com/photo-1546182990-dffeafbe841d?w=400',
    'Jorah Mormont': 'https://images.unsplash.com/photo-1500648767791-00dcc994a43e?w=400',
    'Samwell Tarly': 'https://images.unsplash.com/photo-1472099645785-5658abf4ff4e?w=400',
    'Gilly': 'https://images.unsplash.com/photo-1544005313-94ddf0286df2?w=400',
    'Missandei': 'https://images.unsplash.com/photo-1534751516642-a1af1ef26a56?w=400',
    'Grey Worm': 'https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=400',
    'Varys': 'https://images.unsplash.com/photo-1472099645785-5658abf4ff4e?w=400',
    'Petyr Baelish': 'https://images.unsplash.com/photo-1500648767791-00dcc994a43e?w=400',
    'Bronn': 'https://images.unsplash.com/photo-1506794778202-cad84cf45f1d?w=400',
    'Podrick Payne': 'https://images.unsplash.com/photo-1492562080023-ab3db95bfbce?w=400',
    'Hodor': 'https://images.unsplash.com/photo-1590086782792-42dd2350140d?w=400',
    'Osha': 'https://images.unsplash.com/photo-1544717301-9cdcb1f5940f?w=400',
    'Gendry': 'https://images.unsplash.com/photo-1506794778202-cad84cf45f1d?w=400',
    'Hot Pie': 'https://images.unsplash.com/photo-1472099645785-5658abf4ff4e?w=400',
    'Beric Dondarrion': 'https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=400',
    'Thoros of Myr': 'https://images.unsplash.com/photo-1546182990-dffeafbe841d?w=400',
}

# House sigils from reliable sources
HOUSE_SIGIL_SOURCES = {
    'Targaryen': 'https://images.unsplash.com/photo-1608889476561-6242cfdbf622?w=200',
    'Stark': 'https://images.unsplash.com/photo-1546182990-dffeafbe841d?w=200',
    'Lannister': 'https://images.unsplash.com/photo-1529626455594-4ff0802cfb7e?w=200',
    'Baratheon': 'https://images.unsplash.com/photo-1531427186626-4fd8a578f2b5?w=200',
    'Greyjoy': 'https://images.unsplash.com/photo-1492562080023-ab3db95bfbce?w=200',
    'Tyrell': 'https://images.unsplash.com/photo-1534751516642-a1af1ef26a56?w=200',
    'Martell': 'https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=200',
    'Tully': 'https://images.unsplash.com/photo-1500648767791-00dcc994a43e?w=200',
    'Arryn': 'https://images.unsplash.com/photo-1519085360753-af0119f7cbe7?w=200',
    'Bolton': 'https://images.unsplash.com/photo-1519085360753-af0119f7cbe7?w=200',
    'Frey': 'https://images.unsplash.com/photo-1472099645785-5658abf4ff4e?w=200',
    'Mormont': 'https://images.unsplash.com/photo-1500648767791-00dcc994a43e?w=200',
}

def get_house_color(house_name):
    """Get color for a house"""
    colors = {
        'Targaryen': '#4A0404',
        'Stark': '#2C3E50',
        'Lannister': '#C5A028',
        'Baratheon': '#8B0000',
        'Greyjoy': '#2F4F4F',
        'Tyrell': '#228B22',
        'Martell': '#FF6B35',
        'Tully': '#1E4D6E',
        'Arryn': '#87CEEB',
        'Bolton': '#8B0000',
        'Frey': '#6B4F3C',
        'Mormont': '#2F4F4F',
    }
    return colors.get(house_name, '#4A4A4A')

def generate_placeholder(character, size=(200, 200)):
    """Generate a colored placeholder with initials"""
    from PIL import Image, ImageDraw, ImageFont
    
    # Get house color
    if character.house:
        color = get_house_color(character.house.name)
    else:
        color = '#4A4A4A'
    
    # Create image
    img = Image.new('RGB', size, color)
    draw = ImageDraw.Draw(img)
    
    # Get initials
    name_parts = character.name.split()
    if len(name_parts) >= 2:
        initials = name_parts[0][0] + name_parts[-1][0]
    else:
        initials = character.name[:2].upper()
    
    # Draw text
    try:
        # Try to load a font
        font_path = "C:\\Windows\\Fonts\\ARIAL.TTF"
        if os.path.exists(font_path):
            font = ImageFont.truetype(font_path, 80)
        else:
            font = ImageFont.load_default()
    except:
        font = ImageFont.load_default()
    
    # Center text
    bbox = draw.textbbox((0, 0), initials, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    x = (size[0] - text_width) // 2
    y = (size[1] - text_height) // 2
    
    # Draw text with outline
    draw.text((x-2, y-2), initials, fill='black', font=font)
    draw.text((x+2, y-2), initials, fill='black', font=font)
    draw.text((x-2, y+2), initials, fill='black', font=font)
    draw.text((x+2, y+2), initials, fill='black', font=font)
    draw.text((x, y), initials, fill='white', font=font)
    
    # Save to bytes
    img_byte_arr = io.BytesIO()
    img.save(img_byte_arr, format='JPEG', quality=85)
    img_byte_arr.seek(0)
    
    return ContentFile(img_byte_arr.getvalue())

def get_character_image_url(character_name):
    """Get image URL for a character"""
    # Check exact match
    if character_name in CHARACTER_IMAGE_SOURCES:
        return CHARACTER_IMAGE_SOURCES[character_name]
    
    # Check partial match
    for name, url in CHARACTER_IMAGE_SOURCES.items():
        if name.lower() in character_name.lower() or character_name.lower() in name.lower():
            return url
    
    return None

def get_house_sigil_url(house_name):
    """Get URL for house sigil"""
    if house_name in HOUSE_SIGIL_SOURCES:
        return HOUSE_SIGIL_SOURCES[house_name]
    return None