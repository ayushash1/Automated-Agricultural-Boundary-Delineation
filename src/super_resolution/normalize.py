"""
Normalizes a 3-band GeoTIFF image by scaling pixel values between 0 and 1.
"""

import rasterio
import numpy as np

def normalize_image(input_path, output_path):
    """
    Normalizes a 3-band GeoTIFF image by scaling pixel values between 0 and 1.
    """
    with rasterio.open(input_path) as src:
        image = src.read()
        profile = src.profile

        # Scale pixel values to be between 0 and 1
        min_val = np.min(image)
        max_val = np.max(image)
        scaled_image = (image - min_val) / (max_val - min_val)

        # Save the normalized image
        with rasterio.open(output_path, "w", **profile) as dst:
            dst.write(scaled_image)

if __name__ == "__main__":
    process_all_tiles()
