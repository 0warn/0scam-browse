from PIL import Image, ImageDraw, ImageFont
import os

def create_icon(size):
    try:
        # Create icon with a deep background color
        # Using a slightly larger canvas for the shield to make it feel "fuller"
        img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
        d = ImageDraw.Draw(img)
        
        # Draw a bold shield that fills most of the space
        padding = size // 15
        shield_points = [
            (size // 2, padding), # Top
            (size - padding, padding + size // 4), # Right-Top
            (size - padding, size // 2 + padding), # Right-Bottom
            (size // 2, size - padding), # Bottom
            (padding, size // 2 + padding), # Left-Bottom
            (padding, padding + size // 4) # Left-Top
        ]
        
        # Primary Shield Color (Cyber Purple)
        d.polygon(shield_points, fill=(124, 77, 255), outline=(255, 255, 255), width=size//20)
        
        # Draw a "0" or "S" inside for 0Scam
        try:
            # Try to get a bold font
            font = ImageFont.load_default()
            # For better visuals without specific TTF, we'll draw a white circle/dot
            inner_padding = size // 3
            d.ellipse([inner_padding, inner_padding, size-inner_padding, size-inner_padding], fill=(255, 255, 255))
        except:
            pass

        output_path = 'phishing-ai-detector/extension/icon.png'
        img.save(output_path)
        print(f"Bolder icon generated at {output_path}")
        
    except Exception as e:
        print(f"Error creating icon: {e}")
        # Simple fallback
        img = Image.new('RGB', (size, size), (124, 77, 255))
        img.save('phishing-ai-detector/extension/icon.png')

if __name__ == "__main__":
    create_icon(128)
