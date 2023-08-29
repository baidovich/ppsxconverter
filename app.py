from flask import Flask, request, send_file
import os
import subprocess

app = Flask(__name__)

@app.route('/')
def index():
    return "Welcome to the PPSX to PDF Converter!"

@app.route('/convert', methods=['POST'])
def convert():
    try:
        ppsx_file = request.files['ppsx_file']
        if not ppsx_file:
            return "No PPSX file provided", 400

        # Save the uploaded PPSX file temporarily
        ppsx_path = 'temp.ppsx'

        # Save the uploaded PPSX file
        ppsx_file.save(ppsx_path)

        # Use LibreOffice to convert PPSX to PDF
        cmd = [
            'C:\\Program Files\\LibreOffice\\program\\soffice.bin',
            '--headless', '--convert-to', 'pdf',
            ppsx_path, '--outdir', 'converted_files'  # Output directory
        ]
        subprocess.run(cmd, check=True)

        # Clean up temporary PPSX file
        os.remove(ppsx_path)

        # Return the generated PDF as an attachment
        pdf_path = os.path.join('converted_files', 'temp.pdf')
        return send_file(pdf_path, as_attachment=True)
    except Exception as e:
        return str(e), 500

if __name__ == '__main__':
    os.makedirs('converted_files', exist_ok=True)  # Create 'converted_files' folder
    app.run(host='0.0.0.0', port=5000)
