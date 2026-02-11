import ee
import geemap
import os

# 1. Initialize the Earth Engine library
# If this is your first time, you will need to run ee.Authenticate()
try:
    ee.Initialize()
except Exception as e:
    ee.Authenticate()
    ee.Initialize()

# 2. Define your Region of Interest (ROI)
# Example: A point in San Francisco, buffered to create a small area
roi = ee.Geometry.Point([-122.4194, 37.7749]).buffer(2000)

# 3. select the dataset (e.g., Sentinel-2 Surface Reflectance)
collection = (ee.ImageCollection('COPERNICUS/S2_SR')
              .filterDate('2023-01-01', '2023-12-31')
              .filterBounds(roi)
              .filter(ee.Filter.lt('CLOUDY_PIXEL_PERCENTAGE', 5)))

# Get the least cloudy image and clip it to the ROI
image = collection.sort('CLOUDY_PIXEL_PERCENTAGE').first().clip(roi)

# 4. Set Visualization Parameters (True Color)
vis_params = {
    'min': 0,
    'max': 3000,
    'bands': ['B4', 'B3', 'B2']  # Red, Green, Blue
}

# 5. "Show it": Create an interactive map and add the layer
m = geemap.Map()
m.centerObject(roi, 13)
m.addLayer(image, vis_params, "Sentinel-2 Image")

# Display the map (If running in Jupyter Notebook)
# In a standard script, this line won't pop up a window, but geemap works best in Notebooks.
print("Map created. Check your notebook or output to interact.")
# display(m) # Works in Jupyter/Colab

# 6. "Extract it": Export the image as a GeoTIFF locally
out_dir = os.path.join(os.path.expanduser('~'), 'Downloads')
out_file = os.path.join(out_dir, 'sentinel_export.tif')

print(f"Downloading GeoTIFF to: {out_file}...")

# Select only the RGB bands for the export to keep file size small
# (If you want all data for analysis, remove the .select() part)
geemap.ee_export_image(
    image.select(['B4', 'B3', 'B2']),
    filename=out_file,
    scale=10,  # Sentinel-2 resolution is 10m
    region=roi,
    file_per_band=False
)

print("Download complete!")