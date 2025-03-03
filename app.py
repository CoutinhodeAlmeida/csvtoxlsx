from flask import Flask, request, send_file
import pandas as pd
import io

app = Flask(__name__)

@app.route('/', methods=['GET'])  # Health check route
def home():
    return "CSV to XLSX API is running!"

@app.route('/convert', methods=['POST'])  # Main API endpoint
def convert_csv_to_xlsx():
    try:
        # Get CSV file from request
        if 'file' not in request.files:
            return {"error": "No file part in the request"}, 400

        csv_file = request.files['file']

        if csv_file.filename == '':
            return {"error": "No selected file"}, 400

        # Convert CSV to DataFrame
        df = pd.read_csv(csv_file)

        # Convert DataFrame to XLSX in memory
        output = io.BytesIO()
        with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
            df.to_excel(writer, index=False, sheet_name="Sheet1")

        output.seek(0)

        # Return XLSX as a downloadable file
        return send_file(output, mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                         as_attachment=True, download_name="converted.xlsx")

    except Exception as e:
        return {"error": str(e)}, 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)