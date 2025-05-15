# Liver-Cirrhosis-Prediction

Liver Cirrhosis Stage Classification using Machine Learning

This project uses a Voting Classifier ensemble of CatBoost, XGBoost, and LightGBM to predict the stage of liver cirrhosis based on medical report inputs. It also generates a detailed PDF report with prediction results, confidence scores, and medical insights to assist healthcare professionals in documentation and decision-making.

Problem Statement

Liver cirrhosis is a progressive disease that can be life-threatening if undetected. This machine learning project helps classify the condition into one of the following stages:

Stage 0: No Cirrhosis
Stage 1: Early
Stage 2: Moderate
Stage 3: Severe

Dataset

Source: Kaggle – Liver Cirrhosis Stage Classification
Format: CSV
Features include:

* Age, Gender
* Total & Direct Bilirubin
* Liver Enzymes (ALT, AST, ALP)
* Albumin, Proteins, Platelets
* Albumin/Globulin Ratio

Key Features

* Voting Ensemble Classifier: Combines CatBoost, XGBoost, and LightGBM
* High-accuracy stage classification
* Interactive web form for data input (Flask-based)
* Auto-generated PDF report after prediction
* Clean and professional UI with HTML, CSS, and JavaScript
* Suitable for clinical and telemedicine use

Technologies Used

* Python (via Anaconda)
* Jupyter Notebook
* Flask (for web app)
* Scikit-learn, CatBoost, XGBoost, LightGBM
* Pandas, NumPy, Matplotlib, Seaborn
* ReportLab or FPDF (for PDF generation)

Setup Instructions (Anaconda)

1. Clone the Repository

git clone https://github.com/yourusername/liver-cirrhosis-ml.git
cd liver-cirrhosis-ml

2. Create a New Conda Environment

conda create -n cirrhosis-env python=3.9
conda activate cirrhosis-env

3. Install Required Libraries

conda install pandas numpy scikit-learn matplotlib seaborn flask jupyter -y
pip install catboost xgboost lightgbm fpdf reportlab

Note: CatBoost, XGBoost, and LightGBM require `pip` installation.

4. Launch Jupyter Notebook

jupyter notebook

Or run the Flask app:

python app.py

Model Workflow

* Data Cleaning and Preprocessing
* Feature Scaling and Selection
* Training CatBoost, XGBoost, and LightGBM
* Voting Classifier for final prediction
* Display prediction results on web page
* Generate downloadable PDF report with patient details and prediction insights

PDF Report Includes

* Patient Name and Input Details
* Predicted Liver Cirrhosis Stage
* Model Confidence Score
* Date and Timestamp
* Recommended Notes/Advice

Results

* Achieved high test accuracy with ensemble model
* PDF reports enable better medical record-keeping
* Real-time predictions for healthcare professionals

Future Update

* Deploy on Render or Heroku
* Enhance UI for mobile compatibility
* Add patient login and report history view
* Integrate with cloud-based EMRs
