import os
import rasterio
from rasterio.windows import Window
from itertools import product

# CONFIGURATION
INPUT_FILE = 'sentinel_export.tif'  # Your current 10m file
OUTPUT_DIR = 'tiles_10m/'           # Folder to save small tiles
TILE_SIZE = 128                     # 128x128 pixels (input size for model)

# Create output folder
os.makedirs(OUTPUT_DIR, exist_ok=True)

def tile_image(path, tile_size):
    with rasterio.open(path) as src:
        width = src.width
        height = src.height
        
        # Calculate how many tiles we need
        # We use a generator to loop through the grid
        for i, j in product(range(0, width, tile_size), range(0, height, tile_size)):
            # Define the window (the "cookie cutter")
            # If the image edge is reached, clip the window to fit
            w_width = min(tile_size, width - i)
            w_height = min(tile_size, height - j)
            
            window = Window(col_off=i, row_off=j, width=w_width, height=w_height)
            
            # Read the data in that window
            img_data = src.read(window=window)
            
            # Only save if the tile is the full size (skips tiny edge pieces)
            # This is important for batch processing in AI models
            if img_data.shape[1] == tile_size and img_data.shape[2] == tile_size:
                
                # Copy metadata (geo-coordinates) for this specific tile
                transform = src.window_transform(window)
                profile = src.profile.copy()
                profile.update({
                    'height': tile_size,
                    'width': tile_size,
                    'transform': transform
                })
                
                # Save the tile
                filename = f"tile_{i}_{j}.tif"
                out_path = os.path.join(OUTPUT_DIR, filename)
                
                with rasterio.open(out_path, 'w', **profile) as dst:
                    dst.write(img_data)
                    
        print(f"Success! Tiling complete. Check the '{OUTPUT_DIR}' folder.")

if __name__ == "__main__":
    tile_image(INPUT_FILE, TILE_SIZE)