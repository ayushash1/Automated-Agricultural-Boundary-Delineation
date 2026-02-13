"""
Super Resolution Script
-----------------------
Upscales all GeoTIFF tiles in a folder using bicubic interpolation.
Designed as a placeholder for EDSR model integration.

Input  : data/intermediate/tiles/
Output : data/intermediate/super_resolved/
"""

import os
import rasterio
import numpy as np
import cv2
from rasterio.enums import Resampling


# CONFIG

INPUT_DIR = "data/intermediate/tiles"
OUTPUT_DIR = "data/intermediate/super_resolved"
UPSCALE_FACTOR = 4  # 10m → 2.5m

os.makedirs(OUTPUT_DIR, exist_ok=True)


def super_resolve_tile(input_path, output_path):
    """
    Upscale a single GeoTIFF tile using bicubic interpolation.
    """

    with rasterio.open(input_path) as src:
        # Read all bands
        image = src.read()  # shape: (bands, height, width)
        profile = src.profile

        bands, height, width = image.shape

        new_height = height * UPSCALE_FACTOR
        new_width = width * UPSCALE_FACTOR

        super_resolved = []

        # Upscale each band independently
        for band in image:
            band_upscaled = cv2.resize(
                band,
                (new_width, new_height),
                interpolation=cv2.INTER_CUBIC
            )
            super_resolved.append(band_upscaled)

        super_resolved = np.stack(super_resolved)

        # Update metadata
        profile.update({
            "height": new_height,
            "width": new_width,
            "transform": src.transform * src.transform.scale(
                (width / new_width),
                (height / new_height)
            )
        })

        with rasterio.open(output_path, "w", **profile) as dst:
            dst.write(super_resolved)


def process_all_tiles():
    """
    Loop through all tiles and apply super resolution.
    """

    for filename in os.listdir(INPUT_DIR):
        if filename.endswith(".tif"):
            input_path = os.path.join(INPUT_DIR, filename)
            output_path = os.path.join(OUTPUT_DIR, filename)

            print(f"Processing: {filename}")
            super_resolve_tile(input_path, output_path)

    print("✅ Super-resolution complete for all tiles.")


if __name__ == "__main__":
    process_all_tiles()
