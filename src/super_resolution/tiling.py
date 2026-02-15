import os
import rasterio
from rasterio.windows import Window
from itertools import product

def tile_image(input_path, output_dir, tile_size=128):
    """
    Split a large GeoTIFF into smaller overlapping tiles.
    """
    os.makedirs(output_dir, exist_ok=True)
    
    with rasterio.open(input_path) as src:
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
                print(f"Generating tile: {filename}")
                out_path = os.path.join(output_dir, filename)
                
                with rasterio.open(out_path, 'w', **profile) as dst:
                    dst.write(img_data)
                    
    print(f"Tiling complete for {input_path} -> {output_dir}")

if __name__ == "__main__":
    # Example usage (can be overridden by importing)
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--input', required=True, help='Input GeoTIFF')
    parser.add_argument('--output', required=True, help='Output directory')
    parser.add_argument('--size', type=int, default=128, help='Tile size')
    args = parser.parse_args()
    
    tile_image(args.input, args.output, args.size)