#!/usr/bin/env python3
"""
CLI interface for the Image Changer tool.
Contains all Click command definitions.
"""

import click
from pathlib import Path
from main import create_new_images


@click.group()
def cli():
    """Image modification tool to avoid photo hashing detection."""
    pass


@cli.command()
@click.argument('input_path', type=click.Path(exists=True, file_okay=False, dir_okay=True))
@click.argument('output_path', type=click.Path())
@click.option('--pixel-frequency', default=1000, help='How often to modify pixels (default: 1000)')
@click.option('--pixel-intensity', default=10, help='Intensity of pixel modifications (default: 10)')
@click.option('--crop-percentage', default=0.01, help='Percentage to crop (default: 0.01)')
@click.option('--color-enhancement', default=1.01, help='Color enhancement factor (default: 1.01)')
@click.option('--verbose', '-v', is_flag=True, help='Verbose output')
def modify(input_path, output_path, pixel_frequency, pixel_intensity, crop_percentage, color_enhancement, verbose):
    """
    Modify images with subtle changes to avoid photo hashing detection.

    Takes input folder path and output folder path as arguments.
    """
    if verbose:
        click.echo(f"Input path: {input_path}")
        click.echo(f"Output path: {output_path}")
        click.echo(f"Pixel frequency: {pixel_frequency}")
        click.echo(f"Pixel intensity: {pixel_intensity}")
        click.echo(f"Crop percentage: {crop_percentage}")
        click.echo(f"Color enhancement: {color_enhancement}")

    # Detect if this is aggressive mode based on parameters
    obvious_mode = (pixel_frequency <= 200 or crop_percentage >= 0.20 or color_enhancement >= 1.05)

    if verbose:
        click.echo(f"Mode: {'Aggressive (obvious dots)' if obvious_mode else 'Regular (natural dots)'}")

    # Process images with modifications
    create_new_images(input_path, output_path, color_enhancement, crop_percentage, pixel_frequency, pixel_intensity, obvious_mode)


@cli.command()
@click.argument('path', type=click.Path(exists=True, file_okay=False, dir_okay=True))
@click.option('--verbose', '-v', is_flag=True, help='Verbose output')
def delete(path, verbose):
    """
    Delete all files in the specified folder (but keep the folder).
    """
    path = Path(path)

    if verbose:
        click.echo(f"Deleting files in: {path}")

    # Count files before deletion
    files = [f for f in path.iterdir() if f.is_file()]
    file_count = len(files)

    if file_count == 0:
        click.echo("No files found to delete.")
        return

    # Delete files
    for file_path in files:
        try:
            file_path.unlink()
            if verbose:
                click.echo(f"  ✓ Deleted: {file_path.name}")
        except Exception as e:
            click.echo(f"  ✗ Failed to delete {file_path.name}: {e}")

    click.echo(f"Deleted {file_count} files from {path}")
    click.echo(f"Folder {path} remains intact.")





if __name__ == "__main__":
    cli()
