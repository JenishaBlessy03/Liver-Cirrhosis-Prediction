from flask import Flask, render_template, request, jsonify, send_file
import numpy as np
import joblib
import os
from datetime import datetime
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from io import BytesIO

app = Flask(__name__)

# Load trained model and scaler safely
model_path = "liver_cirrhosis_model.pkl"
scaler_path = "scaler.pkl"

if not os.path.exists(model_path) or not os.path.exists(scaler_path):
    raise RuntimeError("Model or scaler file is missing. Please check the file paths.")

model = joblib.load(model_path)
scaler = joblib.load(scaler_path)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/prediction")
def prediction():
    return render_template("prediction.html")

# ✅ Input Validation Function
def validate_input(data):
    """Validates and processes user input for the model."""
    try:
        patient_name = data.get("patient_name", "Unknown Patient").strip()
        required_fields = [
            "age", "gender", "total_bilirubin", "alk_phos", "albumin",
            "prothrombin", "platelets", "sgot", "cholesterol", "triglycerides",
            "copper", "ascites", "hepatomegaly", "spiders", "edema"
        ]

        # Check for missing fields
        if not all(field in data and str(data[field]).strip() != "" for field in required_fields):
            return None, "Missing required fields. Please fill all fields."

        # Convert data to proper format
        input_data = np.array([[
            float(data["age"]), int(data["gender"]), float(data["total_bilirubin"]),
            float(data["alk_phos"]), float(data["albumin"]), float(data["prothrombin"]),
            float(data["platelets"]), float(data["sgot"]), float(data["cholesterol"]),
            float(data["triglycerides"]), float(data["copper"]), int(data["ascites"]),
            int(data["hepatomegaly"]), int(data["spiders"]), int(data["edema"])
        ]])

        return input_data, patient_name
    except ValueError:
        return None, "Invalid input values. Please enter correct numerical values."

# ✅ Prediction Route
@app.route("/predict", methods=["POST"])
def predict():
    """Handles prediction requests and returns a JSON response."""
    try:
        data = request.json
        input_data, patient_name = validate_input(data)

        if input_data is None:
            return jsonify({"error": patient_name}), 400

        scaled_input = scaler.transform(input_data)
        prediction = int(model.predict(scaled_input)[0])  # Ensure prediction is an integer

        # ✅ Corrected Cirrhosis Stage Mapping
        stage_map = {
            0: "No Cirrhosis.",
            1: "Early Cirrhosis (Stage 1).",
            2: "Moderate Cirrhosis (Stage 2).",
            3: "Severe Cirrhosis (Stage 3)."
        }
        stage = stage_map.get(prediction, "Unknown Stage")

        # ✅ Precautions for each stage
        precautions = {
            "No Cirrhosis.": "Advise the patient to avoid alcohol, maintain a healthy diet, and monitor liver function if at risk.",
            "Early Cirrhosis (Stage 1).": "Recommend salt restriction and regular liver function tests. Assess and manage underlying causes like hepatitis or fatty liver.",
            "Moderate Cirrhosis (Stage 2).": "Start dietary modifications, monitor for ascites or varices, and schedule regular follow-ups. Evaluate for complications.",
            "Severe Cirrhosis (Stage 3).": "Refer to a specialist. Monitor for liver failure symptoms and discuss transplant if needed. Provide intensive supportive care."
        }

        result = {
            "patient_name": patient_name,
            "stage": stage,
            "precautions": precautions.get(stage, "No precautions available."),
            "formData": data
        }

        return jsonify(result)
    except Exception as e:
        return jsonify({"error": f"Prediction failed: {str(e)}"}), 500

# ✅ PDF Generation Route
@app.route("/download_pdf", methods=["POST"])
def download_pdf():
    """Generates a professional PDF report for the patient."""
    try:
        data = request.json
        patient_name = data.get("patient_name", "Unknown_Patient").replace(" ", "_")  # Remove spaces for file safety
        stage = data.get("stage", "Unknown Stage")
        precautions = data.get("precautions", "No precautions available.")
        formData = data.get("formData", {})

        pdf_buffer = BytesIO()
        pdf = SimpleDocTemplate(pdf_buffer, pagesize=letter)
        elements = []
        styles = getSampleStyleSheet()

        # ✅ Add Report Title
        elements.append(Paragraph("<b>Liver Cirrhosis Prediction Report</b>", styles["Title"]))
        elements.append(Spacer(1, 12))

        # ✅ Add Patient Details
        elements.append(Paragraph(f"<b>Patient Name:</b> {patient_name.replace('_', ' ')}", styles["Normal"]))
        elements.append(Paragraph(f"<b>Date:</b> {datetime.now().strftime('%Y-%m-%d , %H:%M:%S')}", styles["Normal"]))
        elements.append(Spacer(1, 12))

        # ✅ Add Prediction Details
        elements.append(Paragraph(f"<b>Predicted Stage:</b> {stage}", styles["Normal"]))
        elements.append(Paragraph(f"<b>Precautions:</b> {precautions}", styles["Normal"]))
        elements.append(Spacer(1, 12))

        # ✅ Add Table with Input Data
        table_data = [["Parameter", "Value"]]
        for key, value in formData.items():
            if key != "patient_name":
                table_data.append([key.replace("_", " ").capitalize(), str(value)])

        table = Table(table_data, colWidths=[250, 250])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.darkblue),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        elements.append(table)
        elements.append(Spacer(1, 20))

        # ✅ Add Footer
        elements.append(Paragraph("<b>Doctor's Signature: ____________________________</b>", styles["Normal"]))

        pdf.build(elements)
        pdf_buffer.seek(0)

        return send_file(pdf_buffer, as_attachment=True, download_name=f"{patient_name}_Liver_Cirrhosis_Report.pdf", mimetype="application/pdf")

    except Exception as e:
        return jsonify({"error": f"PDF generation failed: {str(e)}"}), 500

if __name__ == "__main__":
    app.run(debug=True, port=8000)