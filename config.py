"""
Configuration file for Image Changer.
Loads environment variables from .env file.
"""

import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Default paths
DEFAULT_INPUT_PATH = "/path/to/input/photos"
DEFAULT_OUTPUT_PATH = "./modified_photos"

# Get environment variables with defaults
INPUT_PATH = os.getenv("INPUT_PATH", DEFAULT_INPUT_PATH)
OUTPUT_PATH = os.getenv("OUTPUT_PATH", DEFAULT_OUTPUT_PATH)

# Convert to Path objects
INPUT_PATH = Path(INPUT_PATH)
OUTPUT_PATH = Path(OUTPUT_PATH)

def get_input_path():
    """Get the input path from environment variables."""
    return INPUT_PATH

def get_output_path():
    """Get the output path from environment variables."""
    return OUTPUT_PATH

def validate_paths():
    """Validate that the configured paths exist and are accessible."""
    if not INPUT_PATH.exists():
        print(f"⚠️  Warning: Input path does not exist: {INPUT_PATH}")
        return False

    # Create output directory if it doesn't exist
    OUTPUT_PATH.mkdir(parents=True, exist_ok=True)
    return True
