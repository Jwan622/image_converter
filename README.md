# Image Changer

A Python tool to modify images and avoid photo hashing detection while keeping them visually recognizable.

## What It Does

- **Pixel Changes**: Randomly modifies pixels throughout images
- **Subtle Cropping**: Crops 1% from all sides
- **Color Enhancement**: Slightly increases vibrancy
- **Metadata Removal**: Strips EXIF and other data
- **Hash Verification**: Compares before/after hashes to ensure changes

## Installation

```bash
# Install Poetry (if needed)
curl -sSL https://install.python-poetry.org | python3 -

# Install dependencies
make install
```

## Quick Start

### Test Commands (uses `./hinge_photos_modified` as output)

```bash
# Test regular modification
make test-modify

# Test aggressive modification (20% crop, more pixels)
make test-aggressive

# Clean up test files
make delete PATH=./hinge_photos_modified
```

### Make Commands

```bash
# Regular modification
make modify INPUT=<input_path> OUTPUT=<output_path>

# Aggressive modification
make modify-aggressive INPUT=<input_path> OUTPUT=<output_path>

# Delete files in a folder
make delete PATH=<folder_path>

# Clean all output folders
make clean
```

### CLI Commands

```bash
# Regular modification
poetry run python cli.py modify <input_path> <output_path> --verbose

# Aggressive modification
poetry run python cli.py modify <input_path> <output_path> \
  --pixel-frequency 200 \
  --pixel-intensity 25 \
  --crop-percentage 0.20 \
  --color-enhancement 1.05 \
  --verbose

# Delete files
poetry run python cli.py delete <folder_path> --verbose
```

## Examples

```bash
# Test with sample photos
make test-modify
make delete PATH=./hinge_photos_modified

# Process your own photos
make modify INPUT=/path/to/photos OUTPUT=/path/to/modified
make modify-aggressive INPUT=/path/to/photos OUTPUT=/path/to/aggressive

# Clean up
make clean
```

## Supported Formats

- JPEG (.jpg, .jpeg)
- PNG (.png)
- BMP (.bmp)
- TIFF (.tiff)
- WebP (.webp)

## Requirements

- Python 3.8+
- Poetry for dependency management
