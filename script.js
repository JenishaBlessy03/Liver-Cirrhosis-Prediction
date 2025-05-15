async function submitForm() {
    const patientName = document.getElementById('patient_name').value.trim();
    if (!patientName) {
        alert("Please enter the patient's name.");
        return;
    }

    const formData = {
        patient_name: patientName,
        age: parseFloat(document.getElementById('age').value),
        gender: parseInt(document.getElementById('gender').value),
        total_bilirubin: parseFloat(document.getElementById('total_bilirubin').value),
        alk_phos: parseFloat(document.getElementById('alk_phos').value),
        albumin: parseFloat(document.getElementById('albumin').value),
        prothrombin: parseFloat(document.getElementById('prothrombin').value),
        platelets: parseFloat(document.getElementById('platelets').value),
        sgot: parseFloat(document.getElementById('sgot').value),
        cholesterol: parseFloat(document.getElementById('cholesterol').value),
        triglycerides: parseFloat(document.getElementById('triglycerides').value),
        copper: parseFloat(document.getElementById('copper').value),
        ascites: parseInt(document.getElementById('ascites').value),
        hepatomegaly: parseInt(document.getElementById('hepatomegaly').value),
        spiders: parseInt(document.getElementById('spiders').value),
        edema: parseInt(document.getElementById('edema').value)
    };

    try {
        const response = await fetch('/predict', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(formData)
        });

        const result = await response.json();
        result.patient_name = patientName; // Store patient name in result for PDF naming
        sessionStorage.setItem("predictionResult", JSON.stringify(result));

        document.getElementById('download-pdf').style.display = "block"; // Show download button
    } catch (error) {
        console.error("Error:", error);
        alert("Failed to process the prediction. Please try again.");
    }
}

document.addEventListener("DOMContentLoaded", function () {
    const inputs = document.querySelectorAll("input, select");

    inputs.forEach((input, index) => {
        input.addEventListener("keydown", function (event) {
            if (event.key === "Enter") {
                event.preventDefault(); // Prevent form submission
                const nextInput = inputs[index + 1];
                if (nextInput) {
                    nextInput.focus();
                }
            }
        });
    });
});

async function downloadPDF() {
    const resultData = JSON.parse(sessionStorage.getItem("predictionResult"));

    if (!resultData || !resultData.patient_name) {
        alert("No prediction available! Please predict first.");
        return;
    }

    const patientName = resultData.patient_name.replace(/\s+/g, '_'); // Replace spaces with underscores
    const response = await fetch('/download_pdf', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(resultData)
    });

    const blob = await response.blob();
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `${patientName}_Liver_Cirrhosis_Report.pdf`; // Dynamic filename
    document.body.appendChild(a);
    a.click();
    window.URL.revokeObjectURL(url);
}