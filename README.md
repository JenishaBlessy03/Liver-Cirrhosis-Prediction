# Liver-Cirrhosis-Prediction

Liver Cirrhosis Stage Classification using Machine Learning :

This project uses a Voting Classifier ensemble of CatBoost, XGBoost, and LightGBM to predict the stage of liver cirrhosis based on medical report inputs. It also generates a detailed PDF report with prediction results, confidence scores, and medical insights to assist healthcare professionals in documentation and decision-making.

Problem Statement :

Liver cirrhosis is a progressive disease that can be life-threatening if undetected. This machine learning project helps classify the condition into one of the following stages:

Stage 0: No Cirrhosis
Stage 1: Early
Stage 2: Moderate
Stage 3: Severe

Dataset :

Source: Kaggle – https://www.kaggle.com/datasets/aadarshvelu/liver-cirrhosis-stage-classification
Format: CSV
Features include:

* Age, Gender
* Total & Direct Bilirubin
* Liver Enzymes (ALT, AST, ALP)
* Albumin, Proteins, Platelets
* Albumin/Globulin Ratio

Technologies Used

* Python (via Anaconda)
* Jupyter Notebook
* Flask (for web app)
* Scikit-learn, CatBoost, XGBoost, LightGBM
* Pandas, NumPy, Matplotlib, Seaborn
* ReportLab or FPDF (for PDF generation)

Results

* Achieved high test accuracy with ensemble model
* PDF reports enable better medical record-keeping
* Real-time predictions for healthcare professionals
