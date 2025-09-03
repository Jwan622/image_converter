# Image Changer Makefile
# Convenient commands for image modification

# Load environment variables from .env file
ifneq (,$(wildcard ./.env))
    include .env
    export
endif

.PHONY: help install test clean delete modify modify-aggressive test-modify test-aggressive

# Default target
help:
	@echo "Image Changer - Available Commands:"
	@echo ""
	@echo "  install    - Install dependencies with Poetry"
	@echo "  test       - Run the test example script"
	@echo "  clean      - Clean up output folders"
	@echo "  delete     - Delete files in a folder (usage: make delete PATH=/path/to/folder)"
	@echo "  modify     - Modify images (usage: make modify INPUT=/input/path OUTPUT=/output/path)"
	@echo "  modify-aggressive - Modify images aggressively (usage: make modify-aggressive INPUT=/input/path OUTPUT=/output/path)"
	@echo ""
	@echo "Test Commands (uses INPUT_PATH and OUTPUT_PATH from .env):"
	@echo "  test-modify - Test regular modification with sample photos"
	@echo "  test-aggressive - Test aggressive modification with sample photos"
	@echo ""
	@echo "Examples:"
	@echo "  make modify INPUT=/path/to/input/photos OUTPUT=/path/to/output/photos"
	@echo "  make delete PATH=/path/to/folder"
	@echo "  make clean"

# Install dependencies
install:
	poetry install

# Run test script
test:
	python test_example.py

# Clean up output folders
clean:
	@echo "Cleaning up output folders..."
	rm -rf $(OUTPUT_PATH) ./test_* ./hinge_photos_modified
	@echo "Cleanup complete!"

# Delete files in a folder (but keep the folder)
delete:
	@if [ -z "$(PATH)" ]; then \
		echo "Error: PATH not specified. Usage: make delete PATH=/path/to/folder"; \
		exit 1; \
	fi
	@echo "Deleting files in: $(PATH)"
	poetry run python cli.py delete "$(PATH)" --verbose

# Modify images with default settings
modify:
	@if [ -z "$(INPUT)" ] || [ -z "$(OUTPUT)" ]; then \
		echo "Error: INPUT and OUTPUT not specified."; \
		echo "Usage: make modify INPUT=/input/path OUTPUT=/output/path"; \
		exit 1; \
	fi
	@echo "Modifying images..."
	@echo "Input: $(INPUT)"
	@echo "Output: $(OUTPUT)"
	poetry run python cli.py modify "$(INPUT)" "$(OUTPUT)" --verbose

# Modify images with aggressive settings (20% crop, every 200 pixels, 5% color enhancement)
modify-aggressive:
	@if [ -z "$(INPUT_PATH)" ] || [ -z "$(OUTPUT_PATH)" ]; then \
		echo "Error: INPUT_PATH and OUTPUT_PATH not set in .env file."; \
		echo "Please set these variables in your .env file or use:"; \
		echo "make modify-aggressive INPUT=/input/path OUTPUT=/output/path"; \
		exit 1; \
	fi
	@echo "Modifying images with aggressive settings..."
	@echo "Input: $(INPUT_PATH)"
	@echo "Output: $(OUTPUT_PATH)"
	poetry run python cli.py modify "$(INPUT_PATH)" "$(OUTPUT_PATH)" --pixel-frequency 200 --pixel-delta 25 --crop-percentage 0.20 --color-enhancement 1.05 --verbose

# Test targets with default output folder
test-modify:
	@echo "Testing regular modification (output: $(OUTPUT_PATH))..."
	@echo "Input: $(INPUT_PATH)"
	@echo "Output: $(OUTPUT_PATH)"
	poetry run python cli.py modify "$(INPUT_PATH)" "$(OUTPUT_PATH)" --verbose
	@echo ""
	@echo "✅ Test complete! Photos saved to $(OUTPUT_PATH)"

test-aggressive:
	@echo "Testing aggressive modification (output: $(OUTPUT_PATH))..."
	@echo "Input: $(INPUT_PATH)"
	@echo "Output: $(OUTPUT_PATH)"
	poetry run python cli.py modify "$(INPUT_PATH)" "$(OUTPUT_PATH)" --pixel-frequency 200 --pixel-delta 25 --crop-percentage 0.20 --color-enhancement 1.05 --verbose
	@echo ""
	@echo "✅ Test complete! Photos saved to $(OUTPUT_PATH)"



# Show help by default
.DEFAULT_GOAL := help
