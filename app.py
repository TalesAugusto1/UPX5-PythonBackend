from flask import Flask, request, jsonify
from flask_cors import CORS
import PyPDF2
import tabula

app = Flask(__name__)

CORS(app)  # This will enable CORS for all routes


@app.route('/process-pdf', methods=['POST'])
def process_pdf():
    # Get uploaded PDF data
    pdf_data = request.files['pdf_file']

    # Read PDF content
    pdf_reader = PyPDF2.PdfReader(pdf_data)

    # Try different encodings for tabula.read_pdf
    try:
        # First try UTF-8 encoding (assuming common case)
        tables = tabula.read_pdf(pdf_data, multiple_tables=True, encoding='utf-8')
    except UnicodeDecodeError:
        # If UTF-8 fails, try latin-1 encoding
        try:
            tables = tabula.read_pdf(pdf_data, multiple_tables=True, encoding='latin-1')
        except UnicodeDecodeError:
            # If latin-1 fails, try windows-1252 encoding
            tables = tabula.read_pdf(pdf_data, multiple_tables=True, encoding='windows-1252')
            # You can add more encodings to try here if needed

    # Process and format the extracted data (optional)
    processed_data = []
    for table in tables:
        # Assuming the first table is the one you need
        for row in table.values:
            # Clean the data before converting to JSON
            cleaned_row = []
            for value in row:
                cleaned_value = str(value).replace('...', '')  # Remove ellipsis
                if str(value) == 'NaN':
                    cleaned_value += ' '  # Add space after NaN
                cleaned_row.append(cleaned_value)
            processed_data.append(cleaned_row)

    # Return processed data as JSON
    return jsonify(processed_data)


if __name__ == '__main__':
    app.run(debug=True)
