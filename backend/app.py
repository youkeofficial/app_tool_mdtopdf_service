import os
from flask import Flask, render_template, request, send_file, jsonify
from converter import generate_pdf, PDF_DIR

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/docs')
def docs():
    return render_template('docs.html')

@app.route('/api/v1/convert', methods=['POST'])
def api_convert():
    try:
        md_text = ""
        if request.is_json:
            md_text = request.get_json().get('markdown', '')
        elif 'file' in request.files:
            file = request.files['file']
            if file.filename != '':
                md_text = file.read().decode('utf-8')
        else:
            md_text = request.form.get('markdown', '')

        if not md_text:
            return jsonify({"status": "error", "message": "Contenu vide"}), 400

        fname, fpath = generate_pdf(md_text)
        download_url = f"{request.url_root.rstrip('/')}/download/{fname}"
        
        return jsonify({
            "status": "success",
            "filename": fname,
            "download_url": download_url
        })
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/download/<filename>')
def download(filename):
    return send_file(os.path.join(PDF_DIR, filename), as_attachment=True)

@app.route('/convert', methods=['POST'])
def legacy_convert(): return api_convert()

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5001, debug=False)
