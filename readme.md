# 🛰️ Automated Agricultural Boundary Delineation
### High-Resolution Field Mapping via Sentinel-2 & Deep Learning

This project presents an end-to-end deep learning pipeline for automated agricultural field boundary delineation using Sentinel-2 multispectral satellite imagery. The system enhances 10m resolution satellite imagery using a CNN-based super-resolution model and performs semantic segmentation to extract agricultural field boundaries. The final outputs are GIS-ready vector files suitable for spatial analysis applications.

---

## 🎯 Objectives
* **Enhance Resolution:** Upscale Sentinel-2 imagery from 10m to higher spatial resolution (3m / 1m).
* **Automated Detection:** Automatically detect agricultural field boundaries.
* **GIS Integration:** Generate raster and vector outputs for seamless GIS usage.
* **Performance Evaluation:** Evaluate model performance using standard segmentation metrics.

---

## 📊 Input Data
* **Satellite Source:** Sentinel-2.
* **Format:** GeoTIFF.
* **Spatial Resolution:** 10 meters.
* **Bands Used:**
    * **Red (B4), Green (B3), Blue (B2):** Provide visual context.
    * **Near-Infrared (B8):** Improves vegetation discrimination and boundary detection accuracy.

---

## 🏗️ System Architecture
The pipeline consists of the following five stages:

1.  **Data Preprocessing:** Includes cloud masking, band stacking (RGB + NIR), normalization, and image tiling.
2.  **Super-Resolution:** A CNN-based model that enhances spatial resolution from 10m to 3m/1m.
3.  **Boundary Segmentation:** A U-Net based semantic segmentation model for pixel-wise agricultural boundary detection.
4.  **Post-processing:** Morphological filtering, noise removal, and connected component cleanup.
5.  **Vectorization:** Raster-to-polygon conversion and export to GeoJSON/Shapefile with CRS preservation.

---

## 📂 Project Structure
```text
automated-agricultural-boundary-delineation/
│
├── data/
│   ├── raw/                 # Original GeoTIFF files
│   └── processed/           # Preprocessed and tiled data
│
├── notebooks/
│   └── geotiff_exploration.ipynb
│
├── src/
│   ├── preprocess/          # Data cleaning and normalization
│   ├── super_resolution.py  # CNN model implementation
│   ├── segmentation.py      # U-Net model implementation
│   ├── vectorize.py         # GIS conversion logic
│   ├── evaluate.py          # Performance metrics calculation
│   └── main.py              # Pipeline orchestration
│
├── requirements.txt
└── README.md
```

---

## ⚙️ Installation & Usage

### 1. Create a virtual environment
```shell
python -m venv .venv
source .venv/bin/activate   # macOS/Linux
.venv\Scripts\activate      # Windows
```

### 2. Install dependencies
```shell
pip install -r requirements.txt
```

### 3. Running the Pipeline
Execute the full pipeline with a single command:
```shell
python src/main.py
```
*Outputs will be saved in the `outputs/` directory.*

---

## 📈 Evaluation Metrics
Model performance is evaluated using the following standards:
* **Intersection over Union (IoU)**
* **Precision and Recall**
* **Boundary F1-Score**

*Visual validation can be performed using GIS software such as QGIS.*

---

## 📦 Outputs
* Super-resolved imagery (GeoTIFF).
* Boundary segmentation mask (Raster).
* Vectorized field boundaries (GeoJSON / Shapefile).
* GIS-ready outputs with preserved spatial reference.

---

## ☁️ Cloud Integration (Optional)
The system can be integrated with **Google Cloud Storage (GCS)** for handling large-scale satellite datasets. Data storage and processing can be structured for scalable deployment.

## 📚 References
* Sentinel-2 User Guide
* U-Net: Convolutional Networks for Biomedical Image Segmentation
* Deep Learning Applications in Remote Sensing

---
*This project was developed as part of a technical internship evaluation.*