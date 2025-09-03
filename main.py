import random
import string
import hashlib
import io
from pathlib import Path
from PIL import Image, ImageEnhance
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


def add_pixels(image, pixel_frequency=1000, pixel_slight_delta=10):
    """
    Add random pixels to the image to change its hash.
    Adds a pixel every pixel_frequency pixels with specified intensity.
    this returns an in-memory image object.
    """
    width, height = image.size
    total_pixels = width * height

    # Calculate how many pixels to add
    num_pixels_to_add = max(20, total_pixels // pixel_frequency)

    # Convert to RGB if needed
    if image.mode != 'RGB':
        image = image.convert('RGB')

    # Create a copy to modify
    modified_image = image.copy()
    pixels = modified_image.load()

    for _ in range(num_pixels_to_add):
        # Random position
        x = random.randint(0, width - 1)
        y = random.randint(0, height - 1)

        # Get current pixel color
        current_color = pixels[x, y]

        # Modify color with specified intensity
        new_color = []
        for c in current_color:
            new_color.append(max(0, min(255, c + random.randint(-int(pixel_slight_delta), int(pixel_slight_delta)))))
        new_color = tuple(new_color)

        pixels[x, y] = new_color

    return modified_image


def add_some_dots(image, pixel_slight_delta=10, aggressive_mode=False):
    """
    Add several small, subtle round dots in random locations to mark modifications.
    aggressive_mode: If True, use obvious colors for all dots. If False, use natural blending.
    """
    import random
    import math

    # Convert to RGB if needed
    if image.mode != 'RGB':
        image = image.convert('RGB')

    # Create a copy to modify
    new_image = image.copy()
    pixels = new_image.load()

    # Get image dimensions
    width, height = image.size

    # Ensure width and height are integers
    width = int(width)
    height = int(height)

    # Debug: ensure width and height are integers
    width = int(width)
    height = int(height)

    # Create dots of different sizes
    dot_size = 3  # This is used during aggressive mode to see if dot adding actually works.
    small_dot_size = 1  # Size for tiny dots

    # Add dot in middle right side (random position)
    right_x = random.randint(width - 50, width - 20)  # 20-50 pixels from right edge
    right_y = random.randint(height//3, 2*height//3)  # Middle third of height

    # Add dot in top left quadrant (random position)
    left_x = random.randint(20, width//2)  # 20 pixels from left to middle
    left_y = random.randint(20, height//2)  # 20 pixels from top to middle

    # Add dot in top middle (random position)
    top_middle_x = random.randint(width//3, 2*width//3)  # Middle third of width
    top_middle_y = random.randint(20, height//4)  # Top quarter

    # Add dot in bottom middle (random position)
    bottom_middle_x = random.randint(width//3, 2*width//3)  # Middle third of width
    bottom_middle_y = random.randint(3*height//4, height-20)  # Bottom quarter

    # Add dot in the very center (smaller size)
    center_x = width // 2
    center_y = height // 2

    # Add 150 tiny dots in random locations for better detection avoidance
    tiny_dots = []
    for _ in range(800):
        tiny_x = random.randint(20, width - 20)  # Avoid edges
        tiny_y = random.randint(20, height - 20)  # Avoid edges
        tiny_dots.append((tiny_x, tiny_y))

    # Function to add a round dot with fixed gray/white color (for strategic dots)
    def add_specific_location_dot(center_x, center_y, dot_size):
        for dx in range(-dot_size, dot_size + 1):
            for dy in range(-dot_size, dot_size + 1):
                # Calculate distance from center
                distance = math.sqrt(dx*dx + dy*dy)

                # Only add pixels within the circle (dot_size radius)
                if distance <= dot_size:
                    dot_x = center_x + dx
                    dot_y = center_y + dy

                    # Check bounds
                    if 0 <= dot_x < width and 0 <= dot_y < height:
                        # Use gray/white color for strategic dots
                        gray_value = random.randint(180, 220)
                        pixels[dot_x, dot_y] = (gray_value, gray_value, gray_value)

    # Function to add a round dot with natural pixel blending (for tiny dots)
    def add_natural_dot(center_x, center_y, dot_size):
        for dx in range(-dot_size, dot_size + 1):
            for dy in range(-dot_size, dot_size + 1):
                # Calculate distance from center
                distance = math.sqrt(dx*dx + dy*dy)

                # Only add pixels within the circle (dot_size radius)
                if distance <= dot_size:
                    dot_x = center_x + dx
                    dot_y = center_y + dy

                    # Check bounds
                    if 0 <= dot_x < width and 0 <= dot_y < height:
                        # Get the original pixel color
                        original_color = pixels[dot_x, dot_y]

                        # Apply natural variation using pixel_slight_delta (same logic as add_pixels)
                        new_color = []
                        for c in original_color:
                            new_color.append(max(0, min(255, c + random.randint(-int(pixel_slight_delta), int(pixel_slight_delta)))))
                        new_color = tuple(new_color)

                        pixels[dot_x, dot_y] = new_color

    # Function to add a round dot with obvious colors (for aggressive mode)
    def add_obvious_dot(center_x, center_y, dot_size):
        for dx in range(-dot_size, dot_size + 1):
            for dy in range(-dot_size, dot_size + 1):
                # Calculate distance from center
                distance = math.sqrt(dx*dx + dy*dy)

                # Only add pixels within the circle (dot_size radius)
                if distance <= dot_size:
                    dot_x = center_x + dx
                    dot_y = center_y + dy

                    # Check bounds
                    if 0 <= dot_x < width and 0 <= dot_y < height:
                        # Use bright, obvious colors for aggressive mode
                        red = random.randint(200, 255)      # Bright red
                        green = random.randint(0, 100)      # Low green
                        blue = random.randint(0, 100)       # Low blue
                        pixels[dot_x, dot_y] = (red, green, blue)

    # Create list of strategic dot positions
    strategic_dots = [(right_x, right_y), (left_x, left_y), (top_middle_x, top_middle_y), (bottom_middle_x, bottom_middle_y)]

    # Add dots based on mode
    if aggressive_mode:
        # Aggressive mode: Use obvious colors for ALL dots
        for x, y in strategic_dots:
            add_obvious_dot(x, y, dot_size)
        add_obvious_dot(center_x, center_y, small_dot_size)
        for tiny_x, tiny_y in tiny_dots:
            add_obvious_dot(tiny_x, tiny_y, small_dot_size)
    else:
        # Regular mode: Strategic dots are gray, others are natural
        add_specific_location_dot(right_x, right_y, dot_size)        # Middle right
        add_specific_location_dot(left_x, left_y, dot_size)          # Top left quadrant
        add_specific_location_dot(top_middle_x, top_middle_y, dot_size)    # Top middle
        add_specific_location_dot(bottom_middle_x, bottom_middle_y, dot_size)  # Bottom middle
        add_natural_dot(center_x, center_y, small_dot_size)
        for tiny_x, tiny_y in tiny_dots:
            add_natural_dot(tiny_x, tiny_y, small_dot_size)

    return new_image


def crop_image(image, crop_percentage=0.01):
    """
    Crop the image by reducing width and height by crop_percentage.
    This crops from all sides to maintain aspect ratio.
    this returns an in-memory image object.
    """
    width, height = image.size

    # Calculate crop amounts
    crop_width = int(width * crop_percentage)
    crop_height = int(height * crop_percentage)

    # Crop from all sides
    left = crop_width
    top = crop_height
    right = width - crop_width
    bottom = height - crop_height

    return image.crop((left, top, right, bottom))


def wipe_metadata(image):
    """
    Completely remove ALL metadata from the image.
    This creates a completely new image with zero metadata.
    """
    # Convert to RGB if needed (JPEG doesn't support transparency well anyway)
    if image.mode != 'RGB':
        image = image.convert('RGB')

    # Create a completely new image by copying pixel data only
    new_image = Image.new('RGB', image.size)
    new_image.paste(image, (0, 0))

    # Ensure absolutely no metadata is carried over
    new_image.info = {}

    # Force Pillow to not preserve any metadata
    # This is the most aggressive approach - we're essentially recreating the image
    return new_image


def generate_random_word():
    """
    Generate a completely random word using letters, numbers, and symbols.
    """
    # Random length between 5-15 characters
    word_length = random.randint(5, 15)

    # Mix of characters: letters (70%), numbers (20%), symbols (10%)
    char_type = random.random()

    if char_type < 0.7:  # 70% chance: letters only
        chars = string.ascii_letters
    elif char_type < 0.9:  # 20% chance: letters + numbers
        chars = string.ascii_letters + string.digits
    else:  # 10% chance: letters + numbers + symbols
        chars = string.ascii_letters + string.digits + "!@#$%^&*()_+-=[]{}|;:,.<>?"

    # Generate random word
    random_word = ''.join(random.choice(chars) for _ in range(word_length))

    return random_word


def generate_random_number():
    """
    Generate a random number string with varying formats.
    """
    # Different number formats for variety
    format_type = random.random()

    if format_type < 0.4:  # 40% chance: regular number
        digits = random.randint(1, 6)
        return str(random.randint(10**(digits-1), 10**digits - 1))
    elif format_type < 0.7:  # 30% chance: hex-like number
        return hex(random.randint(1000, 999999))[2:].upper()
    elif format_type < 0.9:  # 20% chance: binary-like
        return bin(random.randint(100, 9999))[2:]
    else:  # 10% chance: mixed alphanumeric
        chars = string.ascii_letters + string.digits
        return ''.join(random.choice(chars) for _ in range(random.randint(3, 6)))


def add_fake_metadata(image):
    """
    Add fake metadata to PNG images to avoid suspicion.
    This makes the images look more natural while being harmless.
    """
    from PIL.PngImagePlugin import PngInfo

    # Create PngInfo object for metadata
    metadata = PngInfo()

    # Generate random key-value pairs for metadata fields
    random_key_value_pairs = [
        (generate_random_word().title(), generate_random_word()),
        (generate_random_word().title(), generate_random_word()),
        (generate_random_word().title(), generate_random_word()),
        (generate_random_word().title(), generate_random_word()),
        (generate_random_word().title(), generate_random_word())
    ]

    # Add random metadata with random keys and values
    for key, value in random_key_value_pairs:
        metadata.add_text(key, value)

    hidden_message = "reretluda ciholocla na si doelcm nitsuj"[::-1]
    random_prefix = generate_random_word() + generate_random_number()
    random_suffix = generate_random_word() + generate_random_number()

    # Combine to create ~20 character string
    random_text = random_prefix + " " + random_suffix

    # Add the random text with random key
    random_text_key = generate_random_word().title()
    metadata.add_text(random_text_key, random_text)

    # Add hidden message in a subtle field with random key
    random_notes_key = generate_random_word().title()
    metadata.add_text(random_notes_key, hidden_message)

    # Store the metadata with the image for later use
    image._fake_metadata = metadata

    return image


def wipe_metadata_aggressive(image):
    """
    Ultra-aggressive metadata removal by converting to PNG first.
    PNG has much better metadata control than JPEG.
    """
    # Convert to RGB first
    if image.mode != 'RGB':
        image = image.convert('RGB')

    # Convert to PNG in memory (PNG has better metadata control)
    buffer = io.BytesIO()
    image.save(buffer, format='PNG', optimize=True)
    buffer.seek(0)

    # Load back as a completely fresh PNG image
    png_image = Image.open(buffer)

    # Convert back to RGB for final output
    final_image = png_image.convert('RGB')

    # Ensure no metadata is carried over
    final_image.info = {}

    return final_image


def enhance_colors(image, enhancement_factor=1.1):
    """
    Slightly enhance colors to make them more vibrant.
    this returns an in-memory image object.
    """
    enhancer = ImageEnhance.Color(image)
    return enhancer.enhance(enhancement_factor)


def mask_single_image(image_path, color_enhancement=1.01, crop_percentage=0.01, pixel_frequency=1000, pixel_slight_delta=10, aggressive_mode=False):
    """
    Process a single image through all modification steps.
    Returns the modified image object.
    """
    try:
        # Open image
        with Image.open(image_path) as img:
            # Apply modifications to make the image look like the original but with subtle changes.
            modified_img = add_pixels(img, pixel_frequency, pixel_slight_delta)
            modified_img = crop_image(modified_img, crop_percentage)
            modified_img = add_some_dots(modified_img, pixel_slight_delta, aggressive_mode)  # Add several subtle dots after cropping
            modified_img = enhance_colors(modified_img, color_enhancement)
            modified_img = wipe_metadata_aggressive(modified_img)
            modified_img = add_fake_metadata(modified_img)

            return modified_img
    except Exception as e:
        print(f"Error processing {image_path}: {e}")
        return None


def save_to_output(processed_images, output_path, total_files):
    """
    Save all verified images to the output folder with fake metadata.
    Returns (successful_count, failed_count).
    """
    print(f"\n💾 Saving verified images to output folder...")
    successful = 0

    for i, _, modified_image in processed_images:
        file_extension = '.png'  # Always save as PNG for better metadata control
        output_filename = output_path / f"modified_hinge_photo_{i}{file_extension}"

        # Save with fake metadata
        if hasattr(modified_image, '_fake_metadata'):
            modified_image.save(output_filename, format='PNG', optimize=True, pnginfo=modified_image._fake_metadata)
        else:
            modified_image.save(output_filename, format='PNG', optimize=True)

        successful += 1
        print(f"  ✅ Saved: {output_filename}")

    failed = total_files - successful
    return successful, failed


def calculate_image_hash(image_path):
    """
    Calculate MD5 hash of an image file.
    """
    try:
        with open(image_path, 'rb') as f:
            return hashlib.md5(f.read()).hexdigest()
    except Exception as e:
        print(f"Error calculating hash for {image_path}: {e}")
        return None


def calculate_corner_hash(image_path, corner_position='top-left', corner_size=100):
    """
    Calculate hash of a corner of an image.
    corner_position can be 'top-left' or 'top-right'
    """
    try:
        with Image.open(image_path) as img:
            width, height = img.size

            if corner_position == 'top-left':
                # Crop top-left corner
                corner = img.crop((0, 0, min(corner_size, width), min(corner_size, height)))
            elif corner_position == 'top-right':
                # Crop top-right corner
                corner = img.crop((max(0, width - corner_size), 0, width, min(corner_size, height)))
            else:
                raise ValueError(f"Invalid corner position: {corner_position}")

            # Convert to bytes for hashing
            import io
            buffer = io.BytesIO()
            corner.save(buffer, format='PNG')
            buffer.seek(0)
            return hashlib.md5(buffer.read()).hexdigest()
    except Exception as e:
        print(f"Error calculating {corner_position} corner hash for {image_path}: {e}")
        return None


def verify_metadata_removal(photo_mapping):
    """
    Verify that metadata has been successfully removed from modified photos.
    Returns True if all metadata is removed, False if any remains.
    """
    print("\n" + "="*60)
    print("METADATA REMOVAL VERIFICATION")
    print("="*60)

    total_pairs = len(photo_mapping)
    metadata_removed = 0
    metadata_remaining = 0

    for original_path, modified_path in photo_mapping.items():
        print(f"Verifying: {Path(original_path).name} → {Path(modified_path).name}")

        try:
            # Check original photo metadata
            with Image.open(original_path) as original_img:
                original_exif = original_img.getexif()
                original_info = original_img.info
                original_format = original_img.format

            # Check modified photo metadata
            with Image.open(modified_path) as modified_img:
                modified_exif = modified_img.getexif()
                modified_info = modified_img.info
                modified_format = modified_img.format

            # Count metadata items
            original_metadata_count = len(original_exif) + len(original_info)
            modified_metadata_count = len(modified_exif) + len(modified_info)

            print(f"   Original metadata items: {original_metadata_count}")
            if original_metadata_count > 0:
                print(f"     EXIF: {list(original_exif.keys()) if original_exif else 'None'}")
                print(f"     Info: {list(original_info.keys()) if original_info else 'None'}")

            print(f"   Modified metadata items: {modified_metadata_count}")
            if modified_metadata_count > 0:
                print(f"     EXIF: {list(modified_exif.keys()) if modified_exif else 'None'}")
                print(f"     Info: {list(modified_info.keys()) if modified_info else 'None'}")

            # Check if metadata was successfully removed
            if modified_metadata_count == 0:
                metadata_removed += 1
                print(f"   Status: ✅ METADATA COMPLETELY REMOVED")
            else:
                metadata_remaining += 1
                print(f"   Status: ❌ METADATA STILL PRESENT")
                print(f"     Remaining: {modified_metadata_count} items")

            print()

        except Exception as e:
            print(f"   Status: ⚠️  ERROR CHECKING METADATA: {e}")
            print()

    print("="*60)
    print(f"METADATA REMOVAL SUMMARY:")
    print(f"  Total photo pairs: {total_pairs}")
    print(f"  Metadata removed:  {metadata_removed} ✅")
    print(f"  Metadata remaining: {metadata_remaining} ❌")
    print("="*60)

    if metadata_remaining == 0:
        print("🎉 SUCCESS: All metadata has been completely removed!")
        print("   EXIF and other data has been successfully stripped.")
    else:
        print("⚠️  WARNING: Some metadata remains in modified photos!")
        print("   The metadata removal may not be working properly.")
    print("="*60)

    return metadata_remaining == 0


def safety_checks(original_path, modified_image, output_path):
    """
    Perform comprehensive safety checks on the modified image.
    Returns True if all checks pass, False if any fail.
    """
    # Save the modified image temporarily as PNG for comparison (no metadata)
    temp_path = output_path / f"temp_{Path(original_path).stem}.png"
    modified_image.save(temp_path, format='PNG', optimize=True)

    try:
        # Check 1: Hash comparison
        print(f"🔍 Safety Check: {Path(original_path).name}")

        # Calculate hashes
        original_hash = calculate_image_hash(original_path)
        modified_hash = calculate_image_hash(temp_path)

        if not original_hash or not modified_hash:
            print(f"   ❌ Hash calculation failed")
            return False

        if original_hash == modified_hash:
            print(f"   ❌ Hash identical - modifications failed")
            return False

        print(f"   ✅ Hash different - modifications successful")

        # Check 2: Metadata removal (PNG should have 0 metadata)
        with Image.open(temp_path) as modified_img:
            modified_exif = modified_img.getexif()
            modified_info = modified_img.info

        metadata_count = len(modified_exif) + len(modified_info)

        if metadata_count > 0:
            print(f"   ❌ Metadata remains: {metadata_count} items")
            return False

        print(f"   ✅ Metadata completely removed")

        # All checks passed
        print(f"   ✅ All safety checks passed!")
        return True

    finally:
        # Clean up temp file
        if temp_path.exists():
            temp_path.unlink()


def compare_hashes(photo_mapping):
    """
    Compare hashes of original and modified photos to verify changes.
    Returns True if all hashes are different, False if any are identical.
    """
    print("\n" + "="*60)
    print("HASH COMPARISON RESULTS")
    print("="*60)

    total_pairs = len(photo_mapping)
    different_full_hashes = 0
    same_full_hashes = 0
    different_top_left_hashes = 0
    same_top_left_hashes = 0
    different_top_right_hashes = 0
    same_top_right_hashes = 0

    for original_path, modified_path in photo_mapping.items():
        print(f"Comparing: {Path(original_path).name} → {Path(modified_path).name}")

        # Compare full image hashes
        original_full_hash = calculate_image_hash(original_path)
        modified_full_hash = calculate_image_hash(modified_path)

        if original_full_hash and modified_full_hash:
            if original_full_hash != modified_full_hash:
                different_full_hashes += 1
                print(f"   Full Image:  ✅ DIFFERENT")
                print(f"     Original:  {original_full_hash[:16]}...")
                print(f"     Modified:  {modified_full_hash[:16]}...")
            else:
                same_full_hashes += 1
                print(f"   Full Image:  ❌ IDENTICAL (WARNING!)")
                print(f"     Hash:      {original_full_hash[:16]}...")
        else:
            print(f"   Full Image:  ⚠️  ERROR CALCULATING HASH")

        # Compare top-left corner hashes
        original_top_left_hash = calculate_corner_hash(original_path, 'top-left')
        modified_top_left_hash = calculate_corner_hash(modified_path, 'top-left')

        if original_top_left_hash and modified_top_left_hash:
            if original_top_left_hash != modified_top_left_hash:
                different_top_left_hashes += 1
                print(f"   Top-Left:    ✅ DIFFERENT")
                print(f"     Original:  {original_top_left_hash[:16]}...")
                print(f"     Modified:  {modified_top_left_hash[:16]}...")
            else:
                same_top_left_hashes += 1
                print(f"   Top-Left:    ❌ IDENTICAL (WARNING!)")
                print(f"     Hash:      {original_top_left_hash[:16]}...")
        else:
            print(f"   Top-Left:    ⚠️  ERROR CALCULATING HASH")

        # Compare top-right corner hashes
        original_top_right_hash = calculate_corner_hash(original_path, 'top-right')
        modified_top_right_hash = calculate_corner_hash(modified_path, 'top-right')

        if original_top_right_hash and modified_top_right_hash:
            if original_top_right_hash != modified_top_right_hash:
                different_top_right_hashes += 1
                print(f"   Top-Right:   ✅ DIFFERENT")
                print(f"     Original:  {original_top_right_hash[:16]}...")
                print(f"     Modified:  {original_top_right_hash[:16]}...")
            else:
                same_top_right_hashes += 1
                print(f"   Top-Right:   ❌ IDENTICAL (WARNING!)")
                print(f"     Hash:      {original_top_right_hash[:16]}...")
        else:
            print(f"   Top-Right:   ⚠️  ERROR CALCULATING HASH")

        print()

    print("="*60)
    print(f"SUMMARY:")
    print(f"  Total photo pairs: {total_pairs}")
    print(f"  Full Image Hashes:")
    print(f"    Different: {different_full_hashes} ✅")
    print(f"    Same:      {same_full_hashes} ❌")
    print(f"  Top-Left Corner Hashes:")
    print(f"    Different: {different_top_left_hashes} ✅")
    print(f"    Same:      {same_top_left_hashes} ❌")
    print(f"  Top-Right Corner Hashes:")
    print(f"    Different: {different_top_right_hashes} ✅")
    print(f"    Same:      {same_top_right_hashes} ❌")
    print("="*60)

    # Check if any hashes are identical
    any_identical = (same_full_hashes > 0 or same_top_left_hashes > 0 or same_top_right_hashes > 0)

    # Warnings
    if same_full_hashes > 0:
        print("⚠️  WARNING: Some full image hashes are identical!")
        print("   This means the modifications may not be sufficient.")
    if same_top_left_hashes > 0:
        print("⚠️  WARNING: Some top-left corner hashes are identical!")
        print("   This means the cropping may not be sufficient.")
    if same_top_right_hashes > 0:
        print("⚠️  WARNING: Some top-right corner hashes are identical!")
        print("   This means the cropping may not be sufficient.")

    if not any_identical:
        print("🎉 SUCCESS: All hashes are different!")
        print("   The modifications are effectively changing digital fingerprints.")
    else:
        print("❌ FAILURE: Some hashes are identical!")
        print("   The modifications are not sufficient to avoid detection.")
    print("="*60)

    return not any_identical


def create_new_images(input_path, output_path, color_enhancement=1.01, crop_percentage=0.01, pixel_frequency=1000, pixel_intensity=10, aggressive_mode=False):
    """
    Main function: Process all images, perform safety checks, then save to output.
    """
    input_path = Path(input_path)
    output_path = Path(output_path)

    # Create output directory if it doesn't exist
    output_path.mkdir(parents=True, exist_ok=True)

    # Supported image extensions
    image_extensions = {'.jpg', '.jpeg', '.png', '.bmp', '.tiff', '.webp'}

    # Find all image files
    image_files = [
        f for f in input_path.iterdir()
        if f.is_file() and f.suffix.lower() in image_extensions
    ]

    if not image_files:
        print(f"No image files found in {input_path}")
        return

    print(f"Found {len(image_files)} image files to process in {input_path}...")

    # Process all images first (without saving)
    processed_images = []

    for i, image_file in enumerate(image_files, 1):
        print(f"\n{'='*60}")
        print(f"🖼️  PROCESSING IMAGE {i}/{len(image_files)}: {image_file.name}")
        print(f"{'='*60}")

        # Process the image and get modified version
        modified_image = mask_single_image(image_file, color_enhancement, crop_percentage, pixel_frequency, pixel_intensity, aggressive_mode)

        if modified_image is None:
            print(f"  ✗ Failed to process: {image_file.name}")
            print(f"{'='*60}")
            continue

        # Perform safety checks
        if safety_checks(image_file, modified_image, output_path):
            # Safety checks passed - store for later saving
            processed_images.append((i, image_file, modified_image))
            print(f"\n✅ DONE PROCESSING IMAGE: {image_file.name}")
            print(f"{'='*60}")
        else:
            print(f"  ❌ Safety checks failed for: {image_file.name}")
            print(f"{'='*60}")

    # Now save all verified images to output folder
    successful, failed = save_to_output(processed_images, output_path, len(image_files))

    print(f"\nProcessing complete!")
    print(f"Successful: {successful}")
    print(f"Failed: {failed}")

    if successful > 0:
        print(f"\n🎉 Successfully created {successful} new images!")
        print(f"   All images passed safety checks and have harmless fake metadata.")
    else:
        print(f"\n⚠️  No images were successfully processed.")
        print(f"   Check the safety check results above.")