#!/usr/bin/env python3
"""
Check metadata on ALL modified photos
"""

from PIL import Image
import os

def check_image_metadata(image_path):
    """Check metadata on a single image"""
    try:
        with Image.open(image_path) as img:
            print(f"\n📸 {os.path.basename(image_path)}:")
            print("=" * 50)
            
            # Check if image has metadata
            if hasattr(img, 'info') and img.info:
                print("✅ Metadata found:")
                for key, value in img.info.items():
                    print(f"   {key}: {value}")
            else:
                print("❌ No metadata found")
                
            # Check image format and size
            print(f"   Format: {img.format}")
            print(f"   Size: {img.size}")
            print(f"   Mode: {img.mode}")
            
    except Exception as e:
        print(f"❌ Error reading {image_path}: {e}")

def main():
    """Check metadata on ALL modified photos"""
    modified_folder = "./modified_photos"
    
    if not os.path.exists(modified_folder):
        print(f"❌ Folder {modified_folder} not found")
        return
    
    # Get all PNG files
    png_files = [f for f in os.listdir(modified_folder) if f.endswith('.png')]
    
    if not png_files:
        print(f"❌ No PNG files found in {modified_folder}")
        return
    
    print(f"🔍 Checking metadata on ALL {len(png_files)} modified photos...")
    
    # Check ALL images
    for i, filename in enumerate(sorted(png_files)):
        image_path = os.path.join(modified_folder, filename)
        check_image_metadata(image_path)
        
        if i < len(png_files) - 1:  # Add separator between images
            print("\n" + "-" * 60)
    
    print(f"\n🎉 Completed! Checked {len(png_files)} photos total.")

if __name__ == "__main__":
    main()
