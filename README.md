# Soil Land Use Classification using Machine Learning

## Overview

This project implements a machine learning pipeline for classifying land use based on geospatial and environmental data. The objective is to predict land use categories by combining raster-derived features, such as elevation, with vector-based soil information.

The project integrates Geographic Information Systems (GIS) preprocessing with supervised machine learning to build a classification model that can support environmental analysis and land management.

## Features

* Preprocessing of raster and vector geospatial data.
* Extraction of environmental variables using zonal statistics.
* Data cleaning and preparation for machine learning.
* Training and evaluation of supervised classification models.
* Performance evaluation using standard classification metrics.

## Project Structure

```text
.
├── data/
│   └── joined_all_tables.csv              # Extracted data
│
├── notebook.ipynb            # Exploratory analysis and model training
│
├── featureExtract/
│   ├── extract_data.py   # Allows the user to extract the data from a gpkg file
│   └── join_data.py      # Allows the user to join the data into a single file
│
├── requirements.txt
├── install.bat           # Creates virtual environment and installs dependencies
└── README.md
```

## Dataset

The model is trained using geospatial information extracted from:

* Digital Elevation Model (DEM)
* Soil classification vector layer
* Additional environmental variables (optional)

Raster values are summarized for each polygon using zonal statistics to generate numerical features for the machine learning model.

## Machine Learning Workflow

1. Load raster and vector datasets.
2. Validate and preprocess spatial data.
3. Extract raster statistics for each polygon.
4. Build the feature dataset.
5. Split the data into training and testing sets.
6. Train the classification model.
7. Evaluate model performance.
8. Save the trained model.

## Technologies

* Python
* scikit-learn
* Pandas
* NumPy
* GeoPandas
* Rasterio
* GDAL
* QGIS
* Matplotlib

## Evaluation Metrics

The model is evaluated using:

* Accuracy
* Precision
* Recall
* F1-Score
* Confusion Matrix

## Installation

Clone the repository:

```bash
git clone https://github.com/nadiejcp/soil-land-use-classification.git
cd soil-land-use-classification
```

Create a virtual environment:

```bash
python -m venv venv
```

Activate it:

**Windows**

```bash
venv\Scripts\activate
```

**Linux / macOS**

```bash
source venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

## Running the Project

Train the model:

```bash
python src/train.py
```

Evaluate the trained model:

```bash
python src/evaluate.py
```

## Future Improvements

* Incorporate additional environmental variables such as precipitation and temperature.
* Compare multiple machine learning algorithms, including XGBoost and LightGBM.
* Integrate satellite imagery features.
* Perform hyperparameter optimization.
* Develop a web application for interactive predictions.

## License

This project is intended for academic and research purposes.
