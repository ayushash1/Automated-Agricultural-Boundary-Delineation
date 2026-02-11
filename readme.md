# Automated Agricultural Boundary Delineation Using Satellite Imagery
# Overview

This project presents an end-to-end deep learning pipeline for automated agricultural field boundary delineation using Sentinel-2 multispectral satellite imagery.

The system enhances 10m resolution satellite imagery using a CNN-based super-resolution model and performs semantic segmentation to extract agricultural field boundaries. The final outputs are GIS-ready vector files suitable for spatial analysis applications.

This project was developed as part of a technical internship evaluation.

# Objective

The objective of this system is to:

Enhance Sentinel-2 imagery from 10m to higher spatial resolution (3m / 1m)

Automatically detect agricultural field boundaries

Generate raster and vector outputs for GIS usage

Evaluate model performance using standard segmentation metrics

# Input Data

Satellite Source: Sentinel-2

Format: GeoTIFF

Spatial Resolution: 10 meters

Bands Used:

Red (B4)

Green (B3)

Blue (B2)

Near-Infrared (B8)

RGB bands provide visual context, while the NIR band improves vegetation discrimination and boundary detection accuracy.

# System Architecture

The pipeline consists of the following stages:

2.  Data Preprocessing

Cloud masking

Band stacking (RGB + NIR)

Normalization

Image tiling

2. Super-Resolution

CNN-based super-resolution model

Enhances spatial resolution from 10m to 3m / 1m

3. Boundary Segmentation

U-Net based semantic segmentation

Pixel-wise agricultural boundary detection

4. Post-processing

Morphological filtering

Noise removal

Connected component cleanup

5. Vectorization

Raster-to-polygon conversion

Export to GeoJSON / Shapefile

CRS preservation for GIS compatibility
```
📂 Project Structure
automated-agricultural-boundary-delineation/
│
├── data/
│   ├── raw/
│   └── processed/
│
├── notebooks/
│   └── geotiff_exploration.ipynb
│
├── src/
│   ├── preprocess/
│   ├── super_resolution.py
│   ├── segmentation.py
│   ├── vectorize.py
│   ├── evaluate.py
│   └── main.py
│
├── requirements.txt
└── README.md
```

## Create a virtual environment:
```shell
python -m venv .venv
source .venv/bin/activate   # macOS/Linux
.venv\Scripts\activate      # Windows
```

## Install dependencies:
```shell
pip install -r requirements.txt
```
## Running the Pipeline

Execute the full pipeline:
```shell
python src/main.py
```

Outputs will be saved in the outputs/ directory.

## Evaluation Metrics

Model performance is evaluated using:

Intersection over Union (IoU)

Precision and Recall

Boundary F1-Score

Visual validation can be performed using GIS software such as QGIS.

## Outputs

Super-resolved imagery (GeoTIFF)

Boundary segmentation mask

Vectorized field boundaries (GeoJSON / Shapefile)

GIS-ready outputs with preserved spatial reference

## Cloud Integration (Optional)

The system can be integrated with Google Cloud Storage (GCS) for handling large-scale satellite datasets. Data storage and processing can be structured for scalable deployment.


##  References

Sentinel-2 User Guide

U-Net: Convolutional Networks for Biomedical Image Segmentation

Deep Learning Applications in Remote Sensing